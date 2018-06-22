from flask import render_template
from KaraokeCompass import app
from flask import request
from KaraokeCompass.Song_filter import filter_songs

import numpy as np


@app.route('/')
@app.route('/input')
def songs_input():
	return render_template("input.html")

@app.route('/output')
def songs_output():
    
    song_title = request.args.get('song_title')
    energy = request.args.get('energy')
    decade = request.args.get('decade')

    results = filter_songs(song_title, energy, decade)
    if type(results) == str:
        return render_template("error.html")
        
    songs = []
    string = "https://open.spotify.com/embed?uri="
	
    for i in range(len(results)):
        url = string + results.iloc[i]['uri'] + "&theme=white"
        songs.append(dict(Song=results.iloc[i]['Song_x'], 
                      Artist=results.iloc[i]['Artist'], 
                      uri=url))
    
    return render_template("output.html", songs=songs)
#    return render_template("output.html", songs=song_results)

