#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Jun 17 06:45:24 2018

Location of functions for accessing Spotify's API to get song ids and 
features

@author: Floreana
"""

import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import spotipy.util as util
import pandas as pd

import sys
direct = '/Users/Floreana/Documents/Jobs/Insight/data/'
sys.path.append(direct) 
from Spotify_user_info import main

sp = spotipy.Spotify() 

# Access my Spotify API id etc.
cid, secret, username, scope, redirect_uri = main()


client_credentials_manager = SpotifyClientCredentials(client_id=cid, 
                                                      client_secret=secret) 
sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)

token = util.prompt_for_user_token(username, scope, client_id=cid, 
                                   client_secret=secret, 
                                   redirect_uri=redirect_uri)

if token:
    sp = spotipy.Spotify(auth=token)

def get_song_codes(data, delim, spotify_limit):
    '''
    Function to access Spotify API and get information & features about songs
    '''

    myAuth="Bearer " + token

    notfound=[]
    song_ids = []

    for line in data:
        l = line.split(delim)
        # If you have any characters after your track title before your 
        # delimiter, add [:-1] (where 1 is equal to the number of 
        #additional characters)
        trackTitle=l[0]     
        # [:-1] removes the newline at the end of every line. Make this 
        # [:-2] if you also have a space at the end of each line
        artist=l[1][:-1]    

        r = sp.search(trackTitle, limit=spotify_limit)

        found = False
        for track in r['tracks']['items']:
            trackArtist = track['artists'][0]['name']
            if (trackArtist.lower()==artist.lower()):
                trackID = track['id']
                trackSong = track['name']
                song_ids.append([trackID, trackSong, trackArtist])
                found = True
                break

        if not found:
        # print '****  Could not find song',trackTitle,'by artist',artist
            notfound.append(trackTitle+delim+artist+'\n')
        else:
             print('Added song',trackTitle,'by artist',artist)

    print("\nSongs not added: ")
    for line in notfound:
        print(line)
    print("\n")

#    else:
#        print("Can't get token for", username)
        
    return(song_ids, notfound)
    
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Get Spotify song IDs for all songs in good_songs.txt, bad_songs.txt and 
# range_songs.txt 
def get_ids(filename):
    
    delim = ';'
    
    datafile = (direct + filename)
    data = open(datafile).readlines()
    # Only check 15 songs for first pass to save time
    song_codes, reject_songs = get_song_codes(data, delim, 15)
    # Check 50 songs if not identified in first pass
    new_song_codes, new_reject_songs = get_song_codes(reject_songs, delim, 50)
    song_list = song_codes + new_song_codes
    
    return song_list

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
def get_song_info(song_id_list):
    '''
    Function to access Spotify API and get information & features about songs
    '''

    track_ids = song_id_list
    
    # Initialize arrays for collecting song data
    information = []
    album_date = []
    explicit = []
    popularity = []
    preview_url = []
    
    for track_id in track_ids:    
        
        # If Spotifiy couldn't identify song, sets ID to 0
        if track_id == '0':
            continue
        
        # Pull all song features 
        song_features = sp.audio_features(track_id)
        information.append(song_features[0])
        
        # Pull information of songs not in song features or the range dataframe
        track_info = sp.track(track_id)
        album_date.append(track_info['album']['release_date'])
        explicit.append(track_info['explicit'])
        popularity.append(track_info['popularity'])
        preview_url.append(track_info['preview_url'])
    
    # Create a song dataframe with track information
    all_information = pd.DataFrame(information)
    song_data_df = pd.DataFrame({'album_date':album_date, 
                                 'popularity':popularity, 'explicit':explicit, 
                                 'preview_url': preview_url})

    song_data_df = pd.concat([song_data_df, all_information], axis=1)
    
    return song_data_df
