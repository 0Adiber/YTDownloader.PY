import requests
import pytube
import os

apikey="AIzaSyA5FU-2tG-eOvIOFccXYap5C-pPZ3zaEzM"
pid="PLw-VjHDlEOgvtnnnqWlTqByAtC7tXBg6D"

def getIDs():
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
            print("got all ids from api")
            break
    return videoIDs

def getPathIds(path):
    already = []
    for root, dirs, files in os.walk(path):
        for file in files:
            if file.endswith(".mp3"):
                already.append(file.split('.mp3')[0])
    return already

def main():
    videoIDs = getIDs()
    print(videoIDs)
    #print(len(videoIDs))
    already = getPathIds('.')
    print(already)

if __name__ == '__main__':
    main()