import discord
import asyncio
from discord import option
import os
from typing import Final
from dotenv import load_dotenv
from asyncyt import AsyncYT, Quality, DownloadConfig, VideoFormat
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
import os
asyncio.set_event_loop(asyncio.new_event_loop())
import pickle
import logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S',
    handlers=[
        logging.FileHandler("app.log"),
        logging.StreamHandler()
    ]
)
logging.info("Script started")

load_dotenv()
TOKEN: Final[str] = os.getenv('DISCORD_TOKEN')
CHANNEL: Final[int] = int(os.getenv('DISCORD_CHANNEL'))
SCOPES = ['https://www.googleapis.com/auth/drive']
PARENT_FOLDER_ID:Final[str] = os.getenv('PARENT_FOLDER_ID')
DRIVE_LINK:Final[str] = os.getenv('DRIVE_LINK')

intents = discord.Intents.default()
client = discord.Bot(intents=intents)

#this ↓ was ai because google hates me and did not do what the tutorial did. not the logging part
def authenticate():
    creds = None

    # Load saved login token
    if os.path.exists("token.pickle"):
        with open("token.pickle", "rb") as token:
            creds = pickle.load(token)
            logging.info("token exists")

    # Login if needed
    if not creds or not creds.valid:
        logging.error("no creds found")
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                "credentials.json",
                SCOPES
            )
            creds = flow.run_local_server(port=0)

        # Save token
        with open("token.pickle", "wb") as token:
            pickle.dump(creds, token)

    return creds

async def upload_video(file_path, name):
    creds = authenticate()

    service = build('drive', 'v3', credentials=creds)

    file_metadata = {
        'name': name,
        'parents': [PARENT_FOLDER_ID]
    }

    media = MediaFileUpload(
        file_path,
        resumable=True
    )

    file = service.files().create(
        body=file_metadata,
        media_body=media,
        fields='id'
    ).execute()

    print("Uploaded file ID:", file.get('id'))
    logging.info(f"Uploaded file ID: {file.get('id')}")

@client.event
async def on_ready():
    channel = client.get_channel(CHANNEL)
    print(f'We have logged in as {client.user}')
    logging.info(f'We have logged in as {client.user}')

@client.slash_command(name="addvideo", description="downloads a youtube video and adds it to a google drive folder")
@option("url")
async def addvideo(ctx, url:str):
    logging.info("command used")
    try:
        await ctx.defer()
    except Exception as e:
        print(f"Error deferring: {e}")
        logging.error(f"Error deferring:{e}")
        return
    
    try:
        ay = AsyncYT()
        info = await ay.get_video_info(url)
        logging.info(url)
        config = DownloadConfig(quality=Quality.HD_1080P, video_format=VideoFormat.MP4)
        await ay.download(url=url, config=config)
        
        #this glob part was also ai because i did not know there were other colons in the world 
        import glob
        downloaded_files = glob.glob("downloads/*.mp4")
        if not downloaded_files:
            raise FileNotFoundError("No MP4 file found in downloads directory")
        
        downloaded_file = max(downloaded_files, key=os.path.getctime)
        
        await upload_video(downloaded_file, info.title)
        await ctx.followup.send(f"{ctx.author.mention}: {info.title} has finished downloading and uploaded to {DRIVE_LINK}")
        print(f"{ctx.author.mention}: {info.title} has finished downloading and uploaded")
    except Exception as e:
        print(f"Error in addvideo: {e}")
        logging.error(f"Error in addvideo: {e}")
        try:
            await ctx.followup.send(f"{ctx.author.mention}: an error has occurred please try again or new url")
        except Exception as follow_error:
            print(f"Error sending followup: {follow_error}")
            logging.error(f"Error sending followup: {follow_error}")

def run():
    client.run(TOKEN)


if __name__ == "__main__":
    run()
