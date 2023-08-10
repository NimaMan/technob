
import os
import youtube_dl
import ffmpeg


class Downloader:
    def __init__(self, output_path):
        self.output_path = output_path

    def download_youtube_link(self, youtube_link):
        """
        Downloads the YouTube video from the given link and returns the path of the downloaded video.
        """
        ydl_opts = {
            'format': 'bestaudio/best',
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'wav',
                'preferredquality': '192',
            }],
            'outtmpl': os.path.join(self.output_path, '%(title)s.%(ext)s')
        }
        with youtube_dl.YoutubeDL(ydl_opts) as ydl:
            info_dict = ydl.extract_info(youtube_link, download=True)
            video_path = os.path.join(self.output_path, f"{info_dict['title']}.wav")
        return video_path

    def extract_audio_from_video(self, video_path):
        """
        Extracts the audio track from the video and saves it as a WAV file.
        """
        audio_file_name = os.path.splitext(os.path.basename(video_path))[0] + ".wav"
        output_file_path = os.path.join(self.output_path, audio_file_name)

        ffmpeg.input(video_path).output(output_file_path).run()
        os.remove(video_path)

    def download_songs(self, urls):
        """
        Downloads songs from the given list of YouTube URLs.
        """
        for url in urls:
            video_path = self.download_youtube_link(url)
            self.extract_audio_from_video(video_path)