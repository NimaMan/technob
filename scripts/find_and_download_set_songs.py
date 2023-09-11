import os 
import pandas as pd
from technob.download.youtube import Downloader as YouTubeDownloader
from technob.audio.search.find_set_songs import find_songs_from_set_with_shazam
from technob.download.soundcloud import search_download_from_soundcloud, download_soundcloud_link 


def get_set_youtube(set_name, link=None, output_path="."):
    downloader = YouTubeDownloader(output_path=os.path.join(output_path, set_name))
    
    if link:
        audio_file_path = downloader.download_youtube_link(link)
    else:
        audio_files = downloader.find_and_download_youtube_link(set_name)
        if audio_files:
            audio_file_path = audio_files[0]
        else:
            print(f"No results found for query: {set_name}")
            return None
    
    return audio_file_path


def get_set_soundcloud(set_name, link="", output_path="."):
    if link:
        audio_path = download_soundcloud_link(link, output_path=output_path)
    else:
        audio_path = search_download_from_soundcloud(set_name, output_path=output_path)
    
    return audio_path


def main(set_name, set_source="soundcloud", song_source="soundcloud", link=None, output_path="."):
    if set_source == "youtube":
        audio_file_path = get_set_youtube(set_name, link=link, output_path=output_path)
    elif set_source == "soundcloud":
        audio_file_path = get_set_soundcloud(set_name, link=link, output_path=output_path)
    else:
        print("Invalid set source. Choose either 'youtube' or 'soundcloud'.")
        return
    
    if not audio_file_path:
        print("Set download failed.")
        return

    songs_in_audio = find_songs_from_set_with_shazam(audio_file_path)
    audio_type = os.path.splitext(audio_file_path)[1]
    songs_in_audio.to_csv(audio_file_path.replace(audio_type, ".csv"), index=False)

    set_download_path = os.path.join(output_path, set_name)
    downloader = YouTubeDownloader(output_path=set_download_path)
    for search_name in songs_in_audio["Song Name"] + " " + songs_in_audio["Artist"]:
        if song_source == "youtube":
            downloader.find_and_download_youtube_link(search_name)
        elif song_source == "soundcloud":
            search_download_from_soundcloud(search_name, output_path=set_download_path)
        else:
            print("Invalid song source. Choose either 'youtube' or 'soundcloud'.")
            return


if __name__ == "__main__":
    # Example usage
    main(set_name="Some Set Name", source="soundcloud")
