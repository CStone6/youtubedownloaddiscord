this creates a discord bot that takes a youtube url and uploads it to google drive to bypass youtube restrictions 

PARENT_FOLDER_ID is the stuff at the end of the url of the folder you need to use an oauth thing with google cloud 

INSTALLATION:

DOWNLOAD REQUIRED FILES: 
so you need ffmpeg ffprobe node and yt-dlp. they appeared when i installed so they might do that for you but not sure 

DOWNLOAD CREDS:
you are required to download creds you need to go to [here](https://console.cloud.google.com) you need to create a new project or use an existing one. After that go to API & Services and make a new OAuth 2.0 Client ID make sure to download the json file. After downloading rename to credentials.json

DISCORD API:
so like google how to make a bot. rename .env.example to .env and fill in DISCORD_TOKEN with the token

GET PARENT_FOLDER_ID:
open the folder on drive and copy all of the weird text after drive.google.com/drive/u/1/folders/ 

GET TOKEN:
run token.py it should open a web page asking to allow access press ok and if you see a file in the folder it worked and you can run the real bot without error (fyi this does use drive storage so you might run out fast)

if there are any bugs or questions i will get back to you in 1 to 100000000 days