
import os
import youtube_dl
import ffmpeg
from pytube import YouTube


class Downloader:
    def __init__(self, output_path):
        self.output_path = output_path

    def download_youtube_link_pytube(self, youtube_link, output_format="wav"):
        try:
            youtube_video = YouTube(youtube_link)
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

    def download_youtube_link(self, youtube_link, output_format="wav", extract_audio=True, keep_video=False):
        video_path = self.download_youtube_link_pytube(youtube_link, output_format=output_format)
        if video_path is None:
            video_path = self.download_youtube_link_youtubedl(youtube_link, output_format=output_format)
        
        if extract_audio:
            self.extract_audio_from_video(video_path, output_format=output_format, keep_video=keep_video)
            audio_file_name = os.path.splitext(os.path.basename(video_path))[0] + f".{output_format}"
            video_path = os.path.join(self.output_path, audio_file_name)

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
        if not keep_video:
            return output_file_path
        os.remove(video_path)

    def download_urls(self, urls, output_format="wav"):
        """
        Downloads songs from the given list of YouTube URLs.
        """
        for url in urls:
            video_path = self.download_youtube_link(url, output_format=output_format)
            self.extract_audio_from_video(video_path, output_format=output_format) 



if __name__ == "__main__":

    downloader = Downloader(output_path="/Users/nimamanaf/Desktop/Music/")
    amber_roos = "https://www.youtube.com/watch?v=GzkugkDQPoM"
    indira_paganotto = "https://www.youtube.com/watch?v=BapBHKMYk0E&t=397s"
    amelie_lens = "https://www.youtube.com/watch?v=_Dy_Cn0HEZU"
    downloader.download_youtube_link(amelie_lens)