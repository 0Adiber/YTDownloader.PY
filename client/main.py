import requests
import pytube
import os
import sys, getopt
import datetime

apikey="AIzaSyA5FU-2tG-eOvIOFccXYap5C-pPZ3zaEzM"

def getPlaylistIDs(pid):
    videoIDs = {}

    nextToken = ""

    cc = 0

    while 1==1:
        URL = "https://www.googleapis.com/youtube/v3/playlistItems?part=contentDetails,snippet&maxResults=50" + "&playlistId=" + pid + "&key=" + apikey + "&pageToken=" + nextToken
        response = requests.get(URL)
        res = response.json()

        if(len(res) == 1):
            res = res["error"]
            res = res["errors"]
            res = res[0]
            print(res["reason"])
            print("PlaylistID: " + pid)
            sys.exit()

        for vid in res["items"]:
            id = vid["contentDetails"]["videoId"]
            title = vid["snippet"]["title"]
            title = title.replace(".", "").replace(",", "").replace(";", "").replace(":", "")
            videoIDs[cc] = [id, title]
            cc+=1

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
                already.append(file.split("." + ending)[0])
    return already

def removeDuplicates(videoIDs, already):
    finalList = videoIDs.copy()
    
    for key,value in videoIDs.items():
        for item in value:
            if item in already:
                del finalList[key]

    return finalList

def downloadMusicList(videoIDs, path):   
    os.makedirs(path+"/download/temp", exist_ok=True)
    for key,value in videoIDs.items():
        yt = pytube.YouTube("https://www.youtube.com/watch?v=" + value[0])
        yt.streams.first().download(path+"/download/temp", yt.streams.first().default_filename.replace("mp4", "").replace(" ", "\\ "))
    print("Downloaded all Videos")

    downloads = getFilesOf(path+"/download/temp","mp4")
	
    os.makedirs(path+"/download/Music", exist_ok=True)

    now = datetime.datetime.now()
    newDir = str(now.year) + "-" + str(now.month) + "-" + str(now.day) + "_" + str(now.hour) + "_" + str(now.minute) + "_" + str(now.second)
    os.makedirs(path+"/download/Music/" + newDir, exist_ok=True)

    for item in downloads:
        cmd = "ffmpeg -i " + "\"" + path+"\\download\\temp\\"+item + ".mp4" + "\" \"" + path+"\\download\\Music\\"+newDir + "\\" +item + ".mp3" + "\""
        os.system(cmd)
        os.remove(path+"/download/temp/"+item+".mp4")
    print("Converted and Deleted all Videos")

def downloadVideoList(videoIDs, path, tres):
    os.makedirs(path+"/download/temp", exist_ok=True)

    for key,value in videoIDs.items():
        yt = pytube.YouTube("https://www.youtube.com/watch?v=" + value[0])
        #yt.streams.first().download(path+"/download/temp", yt.streams.first().default_filename.replace("mp4", "").replace(" ", "\\ "))

        fName = yt.streams.first().default_filename.replace(".mp4", "")

        try:
            yt.streams.filter(res=tres).first().download(path+"/download/temp", "temp_VID")
            yt.streams.first().download(path+"/download/temp","temp_AUD")

            cmd = "ffmpeg -i " + "\"" + path + "\\download\\temp\\temp_VID.mp4\" -i \"" + path + "\\download\\temp\\temp_AUD.mp4\" -c copy -map 0:v:0 -map 1:a:0 -shortest \"" + path + "\\download\\temp\\" + fName + ".mp4\"" 
            os.system(cmd)

            os.remove(path+"/download/temp/temp_VID.mp4")
            os.remove(path+"/download/temp/temp_AUD.mp4")
        except:
            print("Res -> not availbale! : " + tres)
            yt.streams.first().download(path+"/download/temp", fName.replace(" ", "\\ "))

    print("Downloaded all Videos")
    
    downloads = getFilesOf(path+"/download/temp","mp4")
	
    os.makedirs(path+"/download/Video", exist_ok=True)

    now = datetime.datetime.now()
    newDir = str(now.year) + "-" + str(now.month) + "-" + str(now.day) + "_" + str(now.hour) + "_" + str(now.minute) + "_" + str(now.second)
    os.makedirs(path+"/download/Video/" + newDir, exist_ok=True)

    for item in downloads:
        os.rename(path + "/download/temp/" + item + ".mp4", path + "/download/Video/" + newDir + "/" + item + ".mp4")
    print("Moved all Videos to /download/Video/" + newDir + "/")

def useMusic(path, vid):
    print("1")

def useVideo(path, vid):
    print("2")

def useMusicList(path, pid):
    videoIDs = getPlaylistIDs(pid)
    already = getFilesOf('.', "mp3")
    videoIDs = removeDuplicates(videoIDs, already)
    if(len(videoIDs) > 0):
        downloadMusicList(videoIDs, path)
    else:
        print("No new Songs")

def useVideoList(path, pid, res):
    videoIDs = getPlaylistIDs(pid)
    already = getFilesOf('.', "mp4")
    videoIDs = removeDuplicates(videoIDs, already)
    if(len(videoIDs) > 0):
        downloadVideoList(videoIDs, path, res)
    else:
        print("No new Videos")

def main(argv):
    path = os.path.abspath(__file__).replace(__file__, "")[:-1]
    try:
        args = argv.split()
        opts, args = getopt.getopt(args, 'hpsmv', ['id=', 'res='])
    except getopt.GetoptError:
        print("Try the -h parameter")
        sys.exit(2)
    
    tid = "You need to specify a Playlist-ID with --id=<pid/vid>"
    tres = "You need to specify a Resolution with --res=<vidRes>"

    for opt, arg in opts:
        if opt == '-h':
            print("Possible Parameters: \n")
            print("-h : this help page")
            print("-p --id=<pid>: Download a YT-Playlist as mp3s")
            print("-s --id=<pid> --res=<vidRes>: Download a YT-Playlist as mp4s with specified video resolution")
            print("-m --id=<vid>: Download one YT-Video as mp3")
            print("-v --id=<vid> --res=<vidRes>: Download one YT-Video as mp4 with specified video resolution")
            sys.exit()
        elif opt == "--id":
            tid = arg
        elif opt == "--res":
            tres = arg

    if not tres.endswith("p"):
        tres = tres + "p"
    
    for opt, arg in opts:
        if opt == "-p":
            if(len(opts) != 2):
                print("Wrong input, try '-h'")
                return
            useMusicList(path, tid)
        if opt == "-s":
            if(len(opts) != 3):
                print("Wrong input, try '-h'")
                return
            useVideoList(path, tid, tres)
    
    sys.exit()

if __name__ == '__main__':
    param = ""
    for i in sys.argv:
        param = param + i + " "
    param = param.replace(__file__, "")
    main(param)