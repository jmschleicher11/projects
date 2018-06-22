#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Jun 16 08:47:29 2018

Accessing www.myvocalrange.com songs, assigning notes a numeric value for 
ranges, then calling function to get the spotify IDs

"""

import sys
import pandas as pd
import pylast
import matplotlib.pyplot as plt
import seaborn as sns
import requests
from bs4 import BeautifulSoup
from datetime import datetime
import os
import numpy as np

from sklearn.model_selection import train_test_split, cross_val_score
from sklearn import neighbors, datasets, svm, linear_model
from sklearn.neighbors import NearestNeighbors, KNeighborsClassifier
from sklearn.externals import joblib

import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import spotipy.util as util

#from spotify_info import spotify_info_songs

sns.set()

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
def clean_strings(input_list):
    
    final_list = []
    
    for item in input_list: 
        if item.startswith('Range'):
            final_list.append(item[7:])
        else:
            final_list.append(item[1:])

    return final_list
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
def range_song_extractor(gender):
    '''
    Function to extract the songs' artists, high notes, and low notes from the 
    html files from search result pages on www.myvocalrange.com
    '''
    
    range_list = []
    artist_song_list = []
    
    for time in gender:
        page = open(direct + time + ".html")
        soup = BeautifulSoup(page.read(), 'html.parser')
        data = [element.text for element in soup.find_all("b")]
        range_list.append([s for s in data if "Range" in s])
        artist_song_list.append([s for s in data if " - " in s])
    
    flat_range_list = [item for sublist in range_list for item in sublist]
    flat_artist_song_list = [item for sublist in 
                             artist_song_list for item in sublist]
    
    ranges = clean_strings(flat_range_list)
    artists_songs = clean_strings(flat_artist_song_list)

    split_artists_songs=[]
    split_ranges=[]
    for item in artists_songs:
        split_artists_songs.append(item.split(" - "))
    for item in ranges:
        split_ranges.append(item.split("-"))

    ranges_df = pd.DataFrame(split_ranges, columns=['Low_Note', 'High_Note'])
    artist_song_df = pd.DataFrame(split_artists_songs, 
                                  columns=['Artist', 'Song'])
    
    full_df = pd.concat([artist_song_df, ranges_df], axis=1)
    
    full_df = full_df.drop_duplicates()
    
    return(full_df)

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
direct = '/Users/Floreana/Documents/Jobs/Insight/data/'

# Names of files songs broken up by male and female
males = ['1900_M', '1960_M', '1970_M', '1980_M', '1990_M', '2000_M', 
         '2010_M_Dance_Disco', '2010_M_Pop_Ballad', '2010_M_Pure_Guitar', 
         '2010_M_Pure_Piano', '2010_M_Rock_Ballad', '2010_M_Rock_Uptempo', 
         '2010_M_Pop_Rock_Ballad_low', '2010_M_Pop_Rock_Ballad_high', 
         '2010_M_Pop_Rock_Uptempo_low', '2010_M_Pop_Rock_Uptempo_high', 
         '2010_M_Pop_Uptempo_low', '2010_M_Pop_Uptempo_high']

females = ['1900_F', '1960_F', '1970_F', '1980_F', '1990_F', '2000_F', 
           '2010_F_Dance_Disco', '2010_F_Pop_Ballad_high', 
           '2010_F_Pop_Ballad_low', '2010_F_Pop_Rock_Ballad', 
           '2010_F_Pop_Rock_Uptempo', '2010_F_Pure_Guitar', 
           '2010_F_Pure_Piano', '2010_F_Rock_Ballad', '2010_F_Rock_Uptempo', 
           '2010_F_Pop_Uptempo_low', '2010_F_Pop_Uptempo_high']

# Dictionary to numeric values to notes
notes = {'C1': 0, 'C#1': 1, 'Db1': 1, 'D1': 2, 'D#1': 3, 'Eb1': 3, 'E1': 4, 
         'F1': 5, 'F#1': 6, 'Gb1': 6, 'G1': 7, 'G#1': 8, 'Ab1': 8, 'A1': 9, 
         'A#1': 10, 'Bb1': 10, 'B1': 11, 'C2': 12, 'C#2': 13, 'Db2': 13, 
         'D2': 14, 'D#2': 15, 'Eb2': 15, 'E2': 16, 'F2': 17, 'F#2': 18, 
         'Gb2': 18, 'G2': 19, 'G#2': 20, 'Ab2': 20, 'A2': 21, 'A#2': 22, 
         'Bb2': 22, 'B2': 23, 'C3': 24, 'C#3': 25, 'Db3': 25, 'D3': 26, 
         'D#3': 27, 'Eb3': 27, 'E3': 28, 'E#3': 29, 'F3': 29, 'F#3': 30, 
         'Gb3': 30, 'G3': 31, 'G#3': 32, 'Ab3': 32, 'A3': 33, 'A#3': 34, 
         'Bb3': 34, 'B3': 35, 'C4': 36, 'C#4': 37, 'Dd4': 37, 'Db4': 37, 
         'D4': 38, 'D#4': 39, 'Eb4': 39, 'E4': 40, 'F4': 41, 'F#4': 42, 
         'Gb4': 42, 'G4': 43, 'G#4': 44, 'Ab4': 44, 'A4': 45, 'A#4': 46, 
         'Bb4': 46, 'B4': 47, 'Cb5': 47, 'C5': 48, 'C#5': 49, 'Db5': 49, 
         'D5': 50, 'D#5': 51, 'Eb5': 51, 'E5': 52, 'E#5': 53, 'F5': 53, 
         'F#5': 54, 'Gb5': 54, 'G5': 55, 'G#5': 56, 'Ab5': 56, 'A5': 57, 
         'A#5': 58, 'Bb5': 58, 'B5': 59, 'C6': 60, 'C#6': 61, 'Db6': 61, 
         'D6': 62, 'D#6': 63, 'Eb6': 63, 'E6': 64, 'F6': 65, 'F#6': 66, 
         'Gb6': 66, 'G6': 67, 'G#6': 68, 'Ab6': 68, 'A6': 69, 'A#6': 70, 
         'Bb6': 70, 'B6': 71, 'C7': 72, 'C#7': 73, 'Db7': 73, 'D7': 74, 
         'D#7': 75, 'Eb7': 75, 'E7': 76, 'F7': 77, 'F#7': 78, 'Gb7': 78, 
         'G7': 79, 'G#7': 80, 'Ab7': 80, 'A7': 81, 'A#7': 82, 'Bb7': 82, 
         'B7': 83}

# Calculate the ranges of songs
males_df = range_song_extractor(males)
females_df = range_song_extractor(females)

# Mapping numeric values to notes, correcting male ranges
females_df['Low_Value'] = females_df.Low_Note.map(notes)
females_df['High_Value'] = females_df.High_Note.map(notes)
females_df['Gender'] = np.full([len(females_df)], 'F')
# Songs associated with male voices are raised an octave on the website
males_df['Low_Value'] = males_df.Low_Note.map(notes) - 12
males_df['High_Value'] = males_df.High_Note.map(notes) - 12
males_df['Gender'] = np.full([len(males_df)], 'M')

songs_df = pd.concat([females_df, males_df], axis=0)

#songs_df.to_csv((direct + 'all_songs_info.txt'))

# Had to manually edit several songs in all_songs_info.txt to get them in a 
# format recognizable by Spotify. 
new_songs_df = pd.read_csv(direct + 'all_songs_edited.txt')
# Just need the Song and Artist of songs to find in Spotify
new_songs_df.to_csv((direct + 'range_songs.txt'), columns=['Song', 'Artist'], 
                sep=';', index=False, header=False)