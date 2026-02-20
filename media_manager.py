# Copyright (C) 2026 PeruvianWizard.
# All Rights Reserved.
# It may be used however you want as long as it doesn't break a law.

from pytubefix import YouTube
from pytubefix import Playlist
from pytubefix.cli import on_progress
from urllib.parse import urlparse
import subprocess
import os
import random

# Checks if provided text is a valid URL. Returns true if URL is valid or false if otherwise
def check_youtube_url(possible_url):
    try:
        is_url = urlparse(possible_url)
        if all([is_url.scheme, is_url.netloc]):
            if 'youtu.be' in possible_url or 'youtube.com' in possible_url:
                return True
        return False
    except ValueError:
        return False

proxies_list = []

# Downloads media given url into Downloads folder and returns name of downloaded media
def download_media(url, format=''):
    valid_formats = ['M4A', 'MP4']

    # Check that correct format was passed as argument
    if format not in valid_formats:
        raise ValueError(f"Invalid format. Choose from: {valid_formats}")

    yt = YouTube(url, on_progress_callback=on_progress)

    if format == 'M4A':
        print("Downloading audio...")
        ys = yt.streams.filter(only_audio=True).order_by('abr').desc().first()
        ys.download(filename=yt.title +'.m4a', output_path=os.path.join(os.path.expanduser("~"), "Downloads"))
    else:
        print("Downloading video with audio...")
        video_path = os.path.abspath(yt.title+'.mp4')
        audio_path = os.path.abspath(yt.title+'.m4a')
        output_path = os.path.join(os.path.expanduser("~"), "Downloads", yt.title + '.mp4')
        ys = yt.streams.get_highest_resolution(False)
        ys.download(filename=yt.title+'.mp4')
        ys = yt.streams.filter(only_audio=True).order_by('abr').desc().first()
        ys.download(filename=yt.title+'.m4a')

        subprocess.run([
            'ffmpeg', 
            '-i', video_path,
            '-i', audio_path,
            '-c:v', 'copy',
            '-c:a', 'aac',
            '-strict', 'experimental',
            output_path
        ])

        os.remove(video_path)
        os.remove(audio_path)

    return yt.title

# Dowloads a playlist by iterating through each url in a playlist and downloads them one by one
# Uses the download_media function above
def download_playlist(url, format=''):
    valid_formats = ['M4A', 'MP4']

    # Check that correct format was passed as argument
    if format not in valid_formats:
        raise ValueError(f"Invalid format. Choose from: {valid_formats}")
    
    play_list = Playlist(url)

    for link in play_list.video_urls:
        download_media(link, format=format)

    return play_list.owner + " Playlist"