
#%%

import os 
import pandas as pd
from technob.video.youtube import Downloader
from technob.audio.search.find_set_songs import find_songs_from_set_with_shazam



set_link = "https://www.youtube.com/watch?v=8SCM_YeNOos"
output_path = "/Users/nimamanaf/Desktop/Music/Trym" 
set_name = "Boiler Room Manchester 2022"
downloader = Downloader(output_path=os.path.join(output_path, set_name)) 
downloader.download_youtube_link(set_link)

audio_file_path = os.path.join(output_path, set_name, set_name + ".wav")
songs_in_audio = find_songs_from_set_with_shazam(audio_file_path)
#print(songs_in_audio)
# save the results to a csv file in the same directory as the audio file 
songs_in_audio.to_csv(audio_file_path.replace(".wav", ".csv"), index=False)

songs_in_audio["query"] = songs_in_audio["Song Name"] + songs_in_audio["Artist"]

save_dir = os.path.dirname(audio_file_path)
downloader = Downloader(output_path=save_dir) 
for search_name in songs_in_audio["query"].value_counts().index:
    downloader.find_and_download_youtube_link(search_name)