import requests
import pytube
import os

apikey="AIzaSyA5FU-2tG-eOvIOFccXYap5C-pPZ3zaEzM"
pid="PLlwwMhdhODxPng2qnz5QziPfCbIq8j722"

def getPlaylistIDs():
    videoIDs = {}

    nextToken = ""

    cc = 0

    while 1==1:
        URL = "https://www.googleapis.com/youtube/v3/playlistItems?part=contentDetails,snippet&maxResults=50" + "&playlistId=" + pid + "&key=" + apikey + "&pageToken=" + nextToken
        response = requests.get(URL)
        res = response.json()
        
        for vid in res["items"]:
            id = vid["contentDetails"]["videoId"]
            title = vid["snippet"]["title"]
            videoIDs[cc] = [id, title]
            cc+=1
            #print(vid["contentDetails"]["videoId"] + "," + vid["snippet"]["title"])

        try:
            nextToken = res["nextPageToken"]
        except:
            print("Got all Ids from Playlist")
            break
    return videoIDs

def getFilesOf(path,ending):
    already = []
    for root, dirs, files in os.walk(path):
        for file in files:
            if file.endswith("."+ending):
                already.append(file.split("."+ending)[0])
    return already

def removeDuplicates(videoIDs, already):
    finalList = videoIDs.copy()
    
    for key,value in videoIDs.items():
        for item in value:
            if item in already:
                del finalList[key]

    return finalList

def downloadMusic(videoIDs, path):
    os.makedirs(path+"/download/temp", exist_ok=True)
    for key,value in videoIDs.items():
        yt = pytube.YouTube("https://www.youtube.com/watch?v=" + value[0])
        yt.streams.first().download(path+"/download/temp", yt.streams.first().default_filename.replace(" ", "_"))
    print("Downloaded all Videos")
    
    downloads = getFilesOf(path+"/download/temp","mp4")
    print(downloads)
	
    os.makedirs(path+"/download/Music", exist_ok=True)
	
    for item in downloads:
        cmd = "ffmpeg -i " + path+"\\download\\temp\\"+item + ".mp4 " + path+"\\download\\Music\\"+item + ".mp3"
        os.system(cmd)
        os.remove(path+"/download/temp/"+item+".mp4")
    print("Converted and Deleted all Videos")

    

def main():
    videoIDs = getPlaylistIDs()
    already = getFilesOf('.', "mp3")
    videoIDs = removeDuplicates(videoIDs, already)
    downloadMusic(videoIDs, "E:\Adrian\Programmieren\Web\YTDownloader\client")


if __name__ == '__main__':
    main()  