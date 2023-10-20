
import os 
import pandas as pd
import numpy as np
from technob.download.youtube import Downloader 


set_list_path = "/Users/nimamanaf/Desktop/Music/99/Awakenings 2022/U - 999999999 - Awakenings Easter Festival 2022.csv"
df = pd.read_csv(set_list_path)
output_path = "/Users/nimamanaf/Desktop/Music/99/Awakwnings 2022"

# drop duplicates 
df = df.drop_duplicates(subset=["Song Name", "Artist", "Genre"], keep="first") 

downloader = Downloader(output_path=output_path)
for song_name, artist_name, genre_name in zip(df["Song Name"], df["Artist"], df["Genre"]):
    search_query = f"{song_name} {artist_name}" 
    downloader.find_and_download(search_query, download_top_k=1,
                                output_format="wav",
                                artist_name=artist_name,
                                song_name=song_name)
