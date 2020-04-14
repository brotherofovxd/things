from __future__ import unicode_literals
import youtube_dl
from playsound import playsound
import os
import urllib
import requests
from bs4 import BeautifulSoup

play_after_download = False

#youtube search function
def youtube(query):
    linkWord = query.replace(' ', '+')
    url = 'https://www.youtube.com/results?sp=EgIQAQ%253D%253D&search_query=' + linkWord
    page = urllib.request.urlopen(url)
    soup = BeautifulSoup(page.read(), "html.parser")
    vidLink = soup.find("div", {"class": "yt-lockup yt-lockup-tile yt-lockup-video vve-check clearfix"}).get("data-context-item-id")
    return vidLink

#gets user to choose between URl input or search function
try:
    url_or_search = input("For URL input enter 1\nFor Search input enter 2\n")
    if int(url_or_search) == 1:
        #gets url input from user
        url = input("Enter your URL: ")
    else:
        ytsearch = youtube(input("Youtube search: "))
        url = "https://www.youtube.com/watch?v={}".format(ytsearch)
except:
    ytsearch = youtube(input("Youtube search: "))
    url = "https://www.youtube.com/watch?v={}/".format(ytsearch)

print("result: ", url)
#gets filename from the user
filename = str(input("What should I name the file? "))

#ask user if play after download
value = input("Play song after download (y/n)? ")
if value.lower() == "y":
    print("Play song after download: True")
    play_after_download = True
elif value.lower() == "n":
    print("Play song after download: False")
else:
    print("invalid input...\nPlay song after download: False")


#checks if url is valid
if not url.startswith("https://www.youtube.com/watch?v="):
    print("Invalid URL!")
    exit(0)
else:
    try:
        ydl_opts = {
            'outtmpl': '{}'.format(filename),
            #'format': 'bestaudio/best',
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192',
            }],
        }
        with youtube_dl.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])
    except Exception as e:
        print("An error occured, ", e)

if play_after_download:
    print("playing song now!")
    file = "{}.mp3".format(filename)
    if not file.endswith(".mp3"):
        os.rename(file, file+".mp3")
    print("File saved as: "+file)
    playsound(file)
else:
    print("Download complete!")
