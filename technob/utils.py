import os
import pandas as pd


def find_music_files(directory_path, music_extensions=('.mp3', '.wav', '.flac', '.aac', '.ogg', '.m4a')):
    """
    Search for music files within a directory and all its subdirectories.

    :param directory_path: The directory path to search for music files.
    :param music_extensions: A tuple of file extensions to consider as music files.
    :return: A list of paths to the music files found.
    """
    music_files = []
    for root, dirs, files in os.walk(directory_path):
        for file in files:
            if file.lower().endswith(music_extensions):
                music_files.append(os.path.join(root, file))
    return music_files


def check_songs_in_computer(song_data, directory_path):
    """
    Check if songs listed in a DataFrame are present in the given directory path.

    :param song_data 
    :param directory_path: The directory path to search for music files.
    :return: A tuple of two lists: (songs_not_found, songs_found)
    """

    if isinstance(song_data, pd.DataFrame):
        # Get the list of songs from the DataFrame
        songs = song_data["Song"].str.lower().to_list()
    elif isinstance(song_data, list):
        songs = [song.lower() for song in song_data]
    elif isinstance(song_data, str):
        songs = [song_data.lower()]
    else:
        raise TypeError(f"song_data must be a pandas DataFrame or a list of strings, or string Got {type(song_data)} instead.")
    # Find all music files in the computer
    music_files = find_music_files(directory_path)

    # Extract just the filenames without the path and extension for comparison
    local_song_names = {os.path.splitext(os.path.basename(music_file))[0].lower() for music_file in music_files}

    # Check if each song is present or not
    songs_not_found = [song for song in songs if song not in local_song_names]
    songs_found = [song for song in songs if song in local_song_names]

    return songs_not_found, songs_found