#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Jun 17 06:45:24 2018

@author: Floreana
"""


def get_song_codes(datafile, delim, spotify_limit):
    
    data = open(dataFile).readlines()

    myAuth="Bearer " + token

    notfound=[]
    song_ids = []

    if token:
        sp = spotipy.Spotify(auth=token)

        for line in data:
            l = line.split(delim)
            trackTitle=l[0]     ## If you have any characters after your track title before your delimiter, add [:-1] (where 1 is equal to the number of additional characters)
            artist=l[1][:-1]    ## [:-1] removes the newline at the end of every line. Make this [:-2] if you also have a space at the end of each line

            r = sp.search(trackTitle, limit=spotify)

            found = False
            for track in r['tracks']['items']:
                if (track['artists'][0]['name'].lower()==artist.lower()):
                    trackID = track['id']
                    song_ids.append(trackID)
                    found = True
                    break

            if not found:
            # print '****  Could not find song',trackTitle,'by artist',artist
                notfound.append(trackTitle+delim+artist)
             else:

                 print('Added song',trackTitle,'by artist',artist)

        print("\nSongs not added: ")
        for line in notfound:
            print(line)
        print("\n")

    else:
        print("Can't get token for", username)
        
    return(song_ids, notfound)