#!/usr/bin/env python3
# -*- coding: utf-8 -*-

def filter_songs(song_title, energy, decade):
    
    import pandas as pd
    
    direct = '/Users/Floreana/Documents/Jobs/Insight/data/'
    
    all_songs = pd.read_pickle(direct + 'full_range_database.pickle')
    karaoke_songs = pd.read_pickle(direct + 'karaoke_range_database.pickle')
    
    if any(all_songs.Song_x.isin([song_title.upper()])):
    
        song_info = all_songs[all_songs.Song_x.str.lower() == 
                              song_title.lower()]
    else:
        return 'bad song'

#    if len(song_info) > 1:
#        print("Which song did you want?")
#        print()
    
    # Get song range information
    low_value = song_info.Low_Value.values[0]
    high_value = song_info.High_Value.values[0]

    
    # Find the songs within the range of the user's song
    songs_in_range = karaoke_songs.loc[(karaoke_songs.Low_Value >= low_value) & 
                                       (karaoke_songs.High_Value <= high_value)]
    
    user_energy = energy.lower()
    user_decade = decade.lower()
    
    # Energy
    if user_energy == 'high':
        output = songs_in_range.loc[songs_in_range.energy > 0.67]
    elif user_energy == 'medium': 
        output = songs_in_range.loc[(songs_in_range.energy <= 0.67) &
                                    (songs_in_range.energy > 0.33)]
    elif user_energy == 'low':
        output = songs_in_range.loc[songs_in_range.energy <= 0.33]
    else:
        output = songs_in_range
  
#    # Feeling
#    if user_feeling == 'upbeat':
#        output = output.loc[output.valence.values >=0.5]
#    elif user_feeling == 'downbeat':
#        output = output.loc[output.valence.values < 0.5]
#    else: 
#        output = output
#        
#    #print("After Feeling: ", output)
#        
    # Decade
    if user_decade == '1960s':
        output = output.loc[output.album_date.values < 1970]
    elif user_decade == '1970s':
        output = output.loc[(output.album_date.values >= 1970) & 
                                    (output.album_date.values < 1980)]
    elif user_decade == '1980s':
        output = output.loc[(output.album_date.values >= 1980) & 
                                    (output.album_date.values < 1990)]
    elif user_decade == '1990s':
        output = output.loc[(output.album_date.values >= 1990) & 
                                    (output.album_date.values < 2000)]
    elif user_decade == '2000s':
        output = output.loc[(output.album_date.values >= 2000) & 
                                    (output.album_date.values < 2010)]
    elif user_decade == '2010s':
        output = output.loc[output.album_date.values >= 2010]
    else:
        output = output

    
    # Removes original song if part of the list
    output = output[-output.Song_x.isin([song_title.upper()])]
    
    return output
#    print("You should sing: ", output.Song_x.values)