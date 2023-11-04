# %%

import os 
import pandas as pd
import numpy as np
from technob.download.youtube import Downloader 
from technob.download.related_tracks.beat_port import get_related_tracks


urls = {"tech-house": "https://www.beatport.com/genre/tech-house/11/top-100",
        }

genre = "tech-house"
url = urls["tech-house"]

df = get_related_tracks(url)

output_path = f"/Users/nimamanaf/Desktop/Music/bp100-{genre}"
downloader = Downloader(output_path=output_path)
for song_name, artist_name, genre_name in zip(df["Song"], df["Artist"], df["Genre"]):
    search_query = f"{song_name} {artist_name}" 
    downloader.find_and_download(search_query, download_top_k=1,
                                output_format="wav",
                                artist_name=artist_name,
                                song_name=song_name)
