import os
import config
import urllib.request
import urllib.parse
from pytube import YouTube
from bs4 import BeautifulSoup


def DownloadPosters(url,dest, CID):
    urllib.request.urlretrieve(url,dest+CID)

def GetYoutubeURLS(searchText):
    urls = []

    textToSearch = searchText
    query = urllib.parse.quote(textToSearch,safe='')
    url = "https://www.youtube.com/results?search_query=" + query
    response = urllib.request.urlopen(url)
    html = response.read()
    soup = BeautifulSoup(html)
    for vid in soup.findAll(attrs={'class':'yt-uix-tile-link'}):
        if not vid['href'].startswith("https://googleads.g.doubleclick.net/‌​"):
            if 'user' not in str(vid['href']):
                if 'list' not in str(vid['href']):
                    if 'iGm8s3XKWcI' not in str(vid['href']) and 'jRJZthBZOAA' not in str(vid['href']):
                        videoURL = 'http://www.youtube.com' + vid['href']
                        print(videoURL)
                        urls.append(videoURL)

    return urls

def DownloadTrailer(urls, dest, CID):
    for url in urls:
        if len(url) > 5:
            print ('checking ' + dest + CID)
            if not os.path.exists(dest+CID+'.mp4'):
                print('Fetching ' + url)
                yt = YouTube(url)
                print('Finished fetching '+str(yt))

                yt.set_filename(CID)
                yt.get_videos()
                print(yt.videos)
                video = yt.get(config.ConfigVars['VideoFormat'], config.ConfigVars['VideoQuality'])
                video.download(dest)
                return
