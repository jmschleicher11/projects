#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Good/Bad Modeling

"""

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
from datetime import datetime
from dateutil.parser import parse

sns.set()

direct = '/Users/Floreana/Documents/Jobs/Insight/data/'

# Organizing dataframes to use with model
bad_songs = pd.read_pickle(direct + 'all_bad_song_info.pickle')
good_songs = pd.read_pickle(direct + 'all_good_song_info.pickle')

bad_songs['classification'] = np.zeros_like(bad_songs['id'])
good_songs['classification'] = np.ones_like(good_songs['id'])

bad_songs.drop_duplicates('id', keep='last', inplace=True)
good_songs.drop_duplicates('id', keep='last', inplace=True)

# Set all songs that appear in both good and bad songs as good
mixed_songs = bad_songs.loc[bad_songs['id'].isin(good_songs['id'])].copy()
mixed_songs['classification'] = 1
all_songs = pd.concat([good_songs, bad_songs], ignore_index=True)

# Cleaning up the columns for modeling

# Removing columns that are not to be used in the model
all_songs.drop(columns={'preview_url', 'analysis_url', 'id', 'track_href', 
                        'uri'}, inplace=True)
    
all_songs['explicit'] = all_songs['explicit'].astype(int)
all_songs['tempo'] = all_songs['tempo'] / 250  # This is faster than most songs
all_songs['popularity'] = all_songs['popularity'] / 100
all_songs['key'] = all_songs['key'] / 12

# Just get the year of the album for each song
album_year = []
release_date = all_songs['album_date']
for date in release_date:
    album_year.append(parse(date).year)
all_songs['album_date'] = album_year

#plt.figure()
pd.plotting.scatter_matrix(all_songs.drop(columns={'acousticness', 
                                                   'instrumentalness', 'key',
                                                   'liveness', 'type',
                                                   'time_signature', 'mode',
                                                   'loudness'}), alpha=0.2)
    

    
