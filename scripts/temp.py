
import os 
import pandas as pd
import numpy as np
from technob.download.youtube import Downloader


# read the song data
db_path = "/Users/nimamanaf/Library/CloudStorage/OneDrive-KocUniversitesi/ses/techno"
df_db = pd.read_csv(os.path.join(db_path, "sc_db.csv"))

# sort the song data by likes and comments
df_db.sort_values(by=["Likes", "Comments"], ascending=False, inplace=True)
df_db.reset_index(drop=True, inplace=True)

# write the sorted song data to a csv file
df_db.to_csv(os.path.join(db_path, "sc_db_sorted.csv"), index=False)
# get the top 500 songs
top_k = 500
df_db = df_db.iloc[:top_k]

# download the songs 
output_path = "/Users/nimamanaf/Desktop/Music/all"
downloader = Downloader(output_path=output_path)

for song_name, artist_name, song_genre in zip(df_db["Song"], df_db["Artist"], df_db["Genre"]):
    search_query = f"{song_name} {artist_name} {song_genre}" 
    downloader.find_and_download(search_query, download_top_k=1, output_format="wav", artist_name=artist_name)
