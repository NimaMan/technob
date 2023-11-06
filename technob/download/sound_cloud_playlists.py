#%%
import os
import pandas as pd
from sclib import SoundcloudAPI, Track, Playlist


def get_playlist_tracks(playlist_url):
    '''
    Retrieve track details from a SoundCloud playlist.

    Parameters:
    playlist_url (str): The URL or identifier of the SoundCloud playlist.

    Returns:
    pandas.DataFrame: A DataFrame containing the following columns for each track in the playlist:
        - Song: The title of the track.
        - Artist: The artist of the track.
        - Release Date: The release date of the track in 'YYYY-MM-DD' format.
        - Genre: The genre of the track.
        - Play Count: The number of times the track has been played.
        - Likes Count: The number of times the track has been liked.
    '''
    # Initialize the API
    api = SoundcloudAPI()

    # Resolve the playlist from the provided URL
    if playlist_url.startswith('https://soundcloud.com/'):
        playlist = api.resolve(playlist_url)
    else:
        playlist = api.resolve(f'https://soundcloud.com/{playlist_url}')
        playlist = api.resolve(playlist_url)
    # Ensure we have a Playlist object
    assert isinstance(playlist, Playlist)

    # Initialize an empty list to store track data
    track_data = []

    # Iterate over the tracks in the playlist
    for track in playlist:
        # Create a dictionary of the track details. Some other can be added as well
        track_details = {
            'Song': track.title,
            'Artist': track.artist,
            'Release Date': track.release_date.split('T')[0] if track.release_date else None,
            'Genre': track.genre,
            'Play Count': track.playback_count,
            'Likes Count': track.likes_count
        }
        # Append the dictionary to our list
        track_data.append(track_details)

    # Create a DataFrame from our list of track details
    track_df = pd.DataFrame(track_data)

    # Convert 'Release Date' to datetime format (year-month-day)
    track_df['Release Date'] = pd.to_datetime(track_df['Release Date']).dt.strftime('%Y-%m-%d')

    return track_df


if __name__ == "__main__":
    # Get the tracks DataFrame
    from technob.download.youtube import Downloader 
    from technob.utils import check_songs_in_computer
    
    output_path = f"/Users/nimamanaf/Desktop/Music"    
    playlist_url = "https://soundcloud.com/bogdan-ciob-c/sets/dark"
    df = get_playlist_tracks(playlist_url)
    # get the list of all the songs that are in the playlist
    playlist_songs = df["Song"].tolist()
    songs_not_found, downloaded_songs = check_songs_in_computer(playlist_songs, directory_path=output_path)

    output_path = os.path.join(output_path, "Bogdan")
    downloader = Downloader(output_path=output_path)
    for song_name, artist_name in zip(df["Song"], df["Artist"]):
        if song_name.lower() in songs_not_found:
            search_query = f"{song_name} {artist_name}" 
            downloader.find_and_download(search_query, download_top_k=1,
                                        output_format="wav",
                                        artist_name=artist_name,
                                        song_name=song_name)
        else:
            print(f"{song_name} is already downloaded.")