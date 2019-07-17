# YTDownloader
__Main purpose was to download Youtube Playlists and keep your Music Folder up-to-date__

## Functionalities:
  1. Download Music
  2. Download Video
  3. Download Playlists
     1. as Music files
     2. as Video files
### File Extensions:
  1. Music = .mp3
  2. Video = .mp4

## Commands:
  __Base:__ 'py main.py '
  * '-h' -\> _Show Help_
  * '-m --id=\<VIDEO ID\>' -\> _Donwload Video as mp3_
  * '-v --id=\<VIDEO ID\> --res=\<RESOLUTION\>' -\> _Donwload Video as mp4_
  * '-p --id=\<PLAYLIST ID\>' -\> _Donwload Playlist as mp3s_
  * '-s --id=\<PLAYLIST ID\> --res=\<RESOLUTION\>' -\> _Donwload Playlist as mp4s_
  
## IDs and RESOLUTIONs:
### IDs
  __Video or Playlist IDs have to be Public or Unlisted__
  1. Get Video ID:
     1. e.g. `https://www.youtube.com/watch?v=PHgc8Q6qTjc`
     2. Take the strange String after the '?v='
  2. Get Playlist ID:
     1. e.g. `https://www.youtube.com/watch?v=Jkyy4JOu9jE&list=PLYH8WvNV1YEn_iiBMZiZ2aWugQfN1qVfM`
        1. take the strange String after the '&list='
     2. e.g. `https://www.youtube.com/playlist?list=PLztXDHpdUwySiFjXLKUSX_RIOc207g5LJ`
        1. take the strange String after the '?list='
### RESOLUTIONS
  __Resolutions have to be valid (the ones you can choose on YouTube), otherwise it will just download the first Video Source, which is normally 360p__

## CONFIG.JSON
```JSON
{
  "apikey": "{YOUR_GOOGLE_API_KEY}"
}
```
### How to get an API Key:
1. Go to [GOOGLE DEVELOPERS](https://console.developers.google.com)
2. Create a Project in the Dashboard
3. Now Click on Library and Activate the "Youtube Data API v3"
4. Go back to the previous site and click on Credentials
5. Click "Create credentials" and select "API key"
6. Copy the API Key and paste it into the config
7. Additionally:
   1. Restrict Key
   2. Probably Give it a nice name
   3. At "Key restrictions" choose "API restrictions"
   4. Now choose the Youtube Data API as restriction
   
## DEPENDENCIES:
1. Python 3
   1. also install pytube
      1. 'pip install pytube'
   2. also install requests
      1. 'pip install requests'
2. FFMPEG
   1. Have a ffmpeg.(exe) in the folder of the main.py file
      1. [HERE](https://www.ffmpeg.org/download.html)
