import os
import ffmpeg
from pytube import YouTube, Search
import youtube_dl

class Downloader:
    def __init__(self, output_path):
        # Ensure output directory exists
        if not os.path.exists(output_path):
            os.makedirs(output_path)
        self.output_path = output_path

    def download_youtube_link_pytube(self, youtube_link):
        try:
            if not isinstance(youtube_link, YouTube):
                youtube_video = YouTube(youtube_link)
            else:
                youtube_video = youtube_link  
            video = youtube_video.streams.filter(only_audio=True).first()
            video.download(self.output_path)
            return os.path.join(self.output_path, video.default_filename)
        except Exception as e:
            print("pytube error:", e)
            return None

    def download_youtube_link_youtubedl(self, youtube_link, output_format="wav"):
        try:
            ydl_opts = {
                'format': 'bestaudio/best',
                'postprocessors': [{
                    'key': 'FFmpegExtractAudio',
                    'preferredcodec': output_format,
                    'preferredquality': '192',
                }],
                'outtmpl': os.path.join(self.output_path, '%(title)s.%(ext)s')
            }
            with youtube_dl.YoutubeDL(ydl_opts) as ydl:
                info_dict = ydl.extract_info(youtube_link, download=True)
                return os.path.join(self.output_path, f"{info_dict['title']}.{output_format}")
        except Exception as e:
            print("youtube_dl error:", e)
            return None

    def download_youtube_link(self, youtube_link, output_format="wav", keep_video=False):
        video_path = self.download_youtube_link_pytube(youtube_link)
        if video_path is None:
            video_path = self.download_youtube_link_youtubedl(youtube_link, output_format=output_format)
        if video_path is None:
            print("Error downloading the video.")
            return None
        return self.extract_audio_from_video(video_path, output_format=output_format, keep_video=keep_video)

    def extract_audio_from_video(self, video_path, output_format="wav", keep_video=False):
        audio_file_name = os.path.splitext(os.path.basename(video_path))[0] + f".{output_format}"
        output_file_path = os.path.join(self.output_path, audio_file_name)
        ffmpeg.input(video_path).output(output_file_path).run()
        if not keep_video:
            os.remove(video_path)
        return output_file_path

    def download_urls(self, urls, output_format="wav"):
        return [self.download_youtube_link(url, output_format=output_format) for url in urls]

    def find_and_download_youtube_link(self, query="", download_top_k=1):
        search = Search(query)
        results = search.results[:download_top_k]
        downloaded_files = []
        for result in results:
            downloaded_files.append(self.download_youtube_link(result.watch_url))
        return downloaded_files


if __name__ == "__main__":
    from technob.download.set_lists import Tracklist, kobosil, reinier, tale_of_us, charlotte_de_witte, amelie_lens, trym
    
    output_path = "/Users/nimamanaf/Desktop/Music/Trym" 
    set_name = "Extrema 2022"
    set_url = trym[set_name]
    
    output_path = os.path.join(output_path, set_name)
    downloader = Downloader(output_path=output_path) 
    downloader.download_youtube_link(set_url)
    
    #'''
    # download the songs from the tracklist of the set 
    tracklist = Tracklist(trym["Extrema 2022"])
    downloader.download_youtube_link(tracklist.youtube_link)
    for song in tracklist.songs:
        search_name = song.search_name
        downloader.find_and_download_youtube_link(search_name)
    #'''