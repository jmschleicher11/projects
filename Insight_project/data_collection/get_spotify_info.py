#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script to get the IDs and all the song information from Spotify, using 
functions defined in spotify_functions
"""

import pandas as pd
import sys
direct = '/Users/Floreana/Documents/Jobs/Insight/data/'
sys.path.append(direct)  
from spotify_functions import get_ids, get_song_info

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Uncomment below if reading from text files and need Spotify song ID

#bad_songs = get_ids('bad_songs.txt')
#bad_songs_df = pd.DataFrame(bad_songs, columns=['Id', 'Song', 'Artist'])
#bad_songs_df.to_pickle((direct+'bad_id_song_artist.pickle'))

#good_songs = get_ids('good_songs.txt')
#good_songs_df = pd.DataFrame(good_songs, columns=['Id', 'Song', 'Artist'])
#good_songs_df.to_pickle((direct+'good_id_song_artist.pickle'))

#range_songs = get_ids('range_songs.txt')
#range_songs_df = pd.DataFrame(range_songs, columns=['Id', 'Song', 'Artist'])
#range_songs_df.to_pickle((direct+'range_id_song_artist.pickle'))

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Uncomment below if reading from text files with song ID and need all the info

bad_songs_df = pd.read_pickle((direct+'bad_id_song_artist.pickle'))
good_songs_df = pd.read_pickle((direct+'good_id_song_artist.pickle'))
range_songs_df = pd.read_pickle((direct+'range_id_song_artist.pickle'))

all_bad_song_info = get_song_info(pd.Series(bad_songs_df['Id']))
all_bad_song_info.to_pickle((direct+'all_bad_song_info.pickle'))
all_good_song_info = get_song_info(pd.Series(good_songs_df['Id']))
all_good_song_info.to_pickle((direct+'all_good_song_info.pickle'))
all_range_song_info = get_song_info(pd.Series(range_songs_df['Id']))
all_range_song_info.to_pickle((direct+'all_range_song_info.pickle'))
