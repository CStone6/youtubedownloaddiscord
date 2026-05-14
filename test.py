from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
import os
import pickle

SCOPES = ['https://www.googleapis.com/auth/drive']

PARENT_FOLDER_ID = "1J71DXBs1ySpiYLJq4O6rjGym6D-se_ZO"

def authenticate():
    creds = None

    # Load saved login token
    if os.path.exists("token.pickle"):
        with open("token.pickle", "rb") as token:
            creds = pickle.load(token)

    # Login if needed
    if not creds or not creds.valid:
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

def upload_video(file_path, name):
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

upload_video(
    file_path="downloads/Big Shot but Its ✨Teto✨.mp4",
    name="Big Shot but Its ✨Teto✨"
)