
import pandas as pd

from technob.download.youtube import Downloader
from technob.download.related_tracks.beat_port import get_related_tracks 

def scrape_recommended_songs(initial_song, song_db, scrapped_songs, song_db_path, iteration_count, verbose=False):
    if initial_song is not None and iteration_count == 1:
        current_song = initial_song
        current_song_name = initial_song.split("/")[-1]
    else:
        random_song = song_db.sample(weights="Likes").iloc[0]
        current_song_name = random_song["Song"]
        current_song = random_song["Sound_Cloud_Link"]

    if current_song in scrapped_songs:
        current_song = song_db.sample().iloc[0]
        current_song_name = current_song["Song"]
        current_song = current_song["Sound_Cloud_Link"]

    if verbose:
        print(f"iteration {iteration_count} current song: {current_song_name}")

    retried_urls = set()
    retry_count = 0
    max_retries = 5
    try:
        if current_song not in retried_urls or retry_count < max_retries:
            song_data_df = get_related_tracks(current_song)
            if not song_data_df.empty:
                song_db = pd.concat([song_db, song_data_df], ignore_index=True)
                if verbose:
                    print(f"iteration {iteration_count} songs in the database: {len(song_db)}, scrapped_songs: {len(scrapped_songs)}, song_df: {len(song_data_df)}")
            song_db.drop_duplicates(subset=["Song", "Artist"], inplace=True)
            song_db.to_csv(song_db_path, index=False)
            scrapped_songs.add(current_song)
            retried_urls.add(current_song)
            retry_count = 0
    except Exception as e:
        print(f'Error: {e}')
        retry_count += 1

# Usage
initial_song = 'your-initial-song-url'
song_db = pd.DataFrame()  # Initialize with your data
scrapped_songs = set()  # Initialize with your data
db_path = "/Users/nimamanaf/Library/CloudStorage/OneDrive-KocUniversitesi/ses/techno"
    
iteration_count = 1
verbose = True
scrape_recommended_songs(initial_song, song_db, scrapped_songs, song_db_path, iteration_count, verbose)