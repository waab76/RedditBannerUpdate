#!/usr/bin/env python2
#
#   File = wetshaving-01-getWinners.py
#
#   This program is free software: you can redistribute it and/or modify
#   it under the terms of the MIT license.
#
#   This program is distributed in the hope that it will be useful,
#   but WITHOUT ANY WARRANTY; without even the implied warranty of
#   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#   GNU General Public License for more details.
#
############################################################################
#
from gimpfu import *
from BeautifulSoup import BeautifulSoup
from datetime import datetime
import os
import praw
import requests
import reddit_config as cfg

def get_winners(inputImage, inputDrawable, tgtPath):
    existingFiles = os.listdir(tgtPath)

    rws = praw.Reddit(client_id=cfg.client_id,
                         client_secret=cfg.client_secret,
                         user_agent=cfg.user_agent,
                         ).subreddit('wetshaving')

    contestWinners = rws.search(query="weekly contest results", sort="new", time_filter="month")
    for winner in contestWinners:
        titleDate = winner.title[40:]
        winnerDate = datetime.strptime(titleDate, "%B %d, %Y")
        winnerFilename = winnerDate.strftime("%Y-%m-%d") + '.jpg'
        if winnerFilename not in existingFiles:
            firstIndex = winner.selftext.find('1st')
            lastIndex = winner.selftext.find('votes')
            imgurLink = winner.selftext[firstIndex:lastIndex].split(" ")[4]
            print(titleDate + " to be downloaded")
            if imgurLink.find(".jpg")>0:
                downloadImage(imgurLink, os.path.join(tgtPath,winnerFilename))
            else:
                downloadFirstAlbumImage(imgurLink, os.path.join(tgtPath,winnerFilename))
        else:
            print(winnerFilename + " already exists")

def downloadImage(imageUrl, localFileName):
    response = requests.get(imageUrl)
    if response.status_code == 200:
        print('Downloading %s...' % (localFileName))
        with open(localFileName, 'wb') as fo:
                for chunk in response.iter_content(4096):
                    fo.write(chunk)

def downloadFirstAlbumImage(albumUrl, localFileName):
    albumSource = requests.get(albumUrl).text
    soup = BeautifulSoup(albumSource)
    matches = soup.findAll('link', rel='image_src')
    downloadImage(matches[0]['href'], localFileName)

############################################################################

register (
    "python_fu_get_winners",            # Name registered in Procedure Browser
    "Get winning images",               # Widget title
    "Get winning images",               # Help
    "BourbonInExile@gmail.com",         # Author
    "BourbonInExile@gmail.com",         # Copyright Holder
    "Feb 2019",                         # Date
    "<Image>/Reddit/1 - Fetch Winners", # Menu Location
    "",                                 # Image Type - No image required
    [( PF_DIRNAME, "tgtPath", "Working Directory:", "" ),],  # Params
    [],                # Results
    get_winners,       # Matches to name of function being defined
    )   # End register

main()
