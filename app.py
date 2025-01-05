from flask import Flask, request, redirect, session, render_template, url_for
from utils.spotify_utils import get_spotify_tracks, get_spotify_auth_url, get_spotify_token
from utils.youtube_utils import create_youtube_playlist, add_tracks_to_youtube
import os
import requests



app = Flask(__name__)
app.secret_key = 'your_secret_key_here'

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login')
def login():
    return redirect(get_spotify_auth_url())

@app.route('/callback')
def callback():
    session['spotify_token'] = get_spotify_token(request.args.get('code'))
    return redirect(url_for('dashboard'))

@app.route('/dashboard')
def dashboard():
    return render_template('dashboard.html')

@app.route('/convert', methods=['POST'])
def convert():
    spotify_playlist_url = request.form.get('playlist_url')
    tracks = get_spotify_tracks(session['spotify_token'], spotify_playlist_url)
    
    youtube_playlist_id = create_youtube_playlist('leo')
    add_tracks_to_youtube(tracks)
    return f"Playlist created successfully! YouTube Playlist ID: {youtube_playlist_id}"

if __name__ == '__main__':
    app.run(debug=True)


