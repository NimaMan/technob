from technob.video import Downloader


if __name__ == "__main__":

    downloader = Downloader(output_path="/Users/nimamanaf/Desktop/Music/")
    anber_roos = "https://www.youtube.com/watch?v=GzkugkDQPoM"
    from_kobosil_set = "https://www.youtube.com/watch?v=gkXB5lui4mg"
    indira_paganotto = "https://www.youtube.com/watch?v=BapBHKMYk0E&t=397s"
    downloader.download_youtube_link(indira_paganotto)