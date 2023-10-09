
import os 
import pandas as pd
import numpy as np
from technob.download.youtube import Downloader
from technob.download.related_tracks.beat_port import get_related_tracks


# read the song data
#db_path = "/Users/nimamanaf/Library/CloudStorage/OneDrive-KocUniversitesi/ses/techno"
#df_db = pd.read_csv(os.path.join(db_path, "bp100.csv"))

page = 1
url = f"https://www.beatport.com/genre/hard-techno/2/tracks?page={page}&per_page=50"

df_db = get_related_tracks(url)

for page in range(2, 500):
    url = f"https://www.beatport.com/genre/hard-techno/2/tracks?page={page}&per_page=50"
    df = get_related_tracks(url)
    print(len(df))
    df_db = pd.concat([df_db, df], ignore_index=True)

# get the top 500 songs
top_k = -1
df_db = df_db.iloc[:top_k]

# download the songs 
output_path = "/Users/nimamanaf/Desktop/Music/bp500"
downloader = Downloader(output_path=output_path)

for song_name, artist_name, song_genre in zip(df_db["Song"], df_db["Artist"], df_db["Genre"]):
    # replace the special characters with space
    song_name = song_name.replace("/", " ")
    artist_name = artist_name.replace("/", " ")
    song_genre = song_genre.replace("/", " ")

    search_query = f"{song_name} {artist_name} {song_genre}" 
    downloader.find_and_download(search_query, download_top_k=1,
                                  output_format="wav",
                                artist_name=artist_name,
                                song_name=song_name)
