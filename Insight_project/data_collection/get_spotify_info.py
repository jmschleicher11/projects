#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Jun 16 10:02:14 2018

@author: Floreana
"""

import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import spotipy.util as util
import pandas as pd

import sys  
sys.path.append('/Users/Floreana/Documents/Jobs/Insight/data/')  
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
else:
    print("Can't get token for", username)

def spotify_info_songs(song_id_list):
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
