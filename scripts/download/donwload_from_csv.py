
import os 
import pandas as pd
import numpy as np
from technob.download.youtube import Downloader 


genre = "tech-house"

csv_path = f"technob/data/bp100-{genre}.csv"
df = pd.read_csv(csv_path)
output_path = f"/Users/nimamanaf/Desktop/Music/bp100-{genre}"

# drop duplicates 
df = df.drop_duplicates(subset=["Song", "Artist", "Genre"], keep="first") 

downloader = Downloader(output_path=output_path)
for song_name, artist_name, genre_name in zip(df["Song"], df["Artist"], df["Genre"]):
    search_query = f"{song_name} {artist_name}" 
    downloader.find_and_download(search_query, download_top_k=1,
                                output_format="wav",
                                artist_name=artist_name,
                                song_name=song_name)
