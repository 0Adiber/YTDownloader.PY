import requests

apikey="AIzaSyA5FU-2tG-eOvIOFccXYap5C-pPZ3zaEzM"
pid="PLw-VjHDlEOgvtnnnqWlTqByAtC7tXBg6D"

videoIDs = []

nextToken = ""

while 1==1:
    URL = "https://www.googleapis.com/youtube/v3/playlistItems?part=contentDetails&maxResults=50" + "&playlistId=" + pid + "&key=" + apikey + "&pageToken=" + nextToken
    response = requests.get(URL)
    res = response.json()
    
    for vid in res["items"]:
        videoIDs.append(vid["contentDetails"]["videoId"])
        print(vid["contentDetails"]["videoId"])

    try:
        nextToken = res["nextPageToken"]
    except:
        print("fertig")
        break

print(len(videoIDs))