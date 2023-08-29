
import os
import ffmpeg
from pytube import YouTube, Search


class Downloader:
    def __init__(self, output_path):
        # create the output path if it doesn't exist
        if not os.path.exists(output_path):
            os.makedirs(output_path)
        self.output_path = output_path

    def download_youtube_link_pytube(self, youtube_link, output_format="wav"):
        try:
            # check if the youtube link is str or YouTube object
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
        """
        Downloads the YouTube video from the given link and returns the path of the downloaded video.

        Parameters:
            youtube_link (str): Link to the YouTube video.
            output_file_name (str, optional): Name of the output file. Default is None (use the title of the video).
            output_format (str, optional): Format of the output file. Default is "wav".

        Returns:
            str: Path to the downloaded video.
        """
        try:
            import youtube_dl
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
                video_path = os.path.join(self.output_path, f"{info_dict['title']}.{output_format}")
                return video_path
        except Exception as e:
            print("youtube_dl error:", e)
            return None
    def download_youtube_link(self, youtube_link, output_format="wav", keep_video=False):
        video_path = self.download_youtube_link_pytube(youtube_link, output_format=output_format)
        if video_path is None:
            video_path = self.download_youtube_link_youtubedl(youtube_link, output_format=output_format)
        if video_path is None:
            print("Error downloading the video.")
            return None
        self.extract_audio_from_video(video_path, output_format=output_format, keep_video=keep_video)
        return video_path

    def extract_audio_from_video(self, video_path, output_audio_name=None, output_format="wav", keep_video=False):
        """
        Extracts the audio track from the video and saves it as a WAV file.
        #TODO: Add support for other audio formats. 
        """
        if not output_audio_name:
            audio_file_name = os.path.splitext(os.path.basename(video_path))[0] + f".{output_format}"
        output_file_path = os.path.join(self.output_path, audio_file_name)

        ffmpeg.input(video_path).output(output_file_path).run()
        if keep_video:
            return output_file_path
        os.remove(video_path)

    def download_urls(self, urls, output_format="wav"):
        """
        Downloads songs from the given list of YouTube URLs.
        """
        for url in urls:
            video_path = self.download_youtube_link(url, output_format=output_format)
            self.extract_audio_from_video(video_path, output_format=output_format) 

    def find_and_download_youtube_link(self, query="", dowonload_top_k=1):
    
        search = Search(query)
        results = search.results 

        for r in results[:dowonload_top_k]:
            self.download_youtube_link(r)

        print(f"Results for {query}")    
        for link in results[:dowonload_top_k]:
            print(link.title)
        return [link.watch_url for link in results]


if __name__ == "__main__":
    from technob.video.set_lists import Tracklist, kobosil, reinier, tale_of_us, charlotte_de_witte, amelie_lens
    
    output_path = "/Users/nimamanaf/Desktop/Music/" 
    set_name = "Amelia Lens - Tomorrowland 2023"
    output_path = os.path.join(output_path, set_name)
    downloader = Downloader(output_path=output_path) 
    
    # download the songs from the tracklist of the set 
    amelie_lens_tracklist = Tracklist(amelie_lens["Tomorrowland Summer 2023"])
    downloader.download_youtube_link(amelie_lens_tracklist.youtube_link)
    for song in amelie_lens_tracklist.songs:
        search_name = song.search_name
        downloader.find_and_download_youtube_link(search_name)