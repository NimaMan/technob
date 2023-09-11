
import os
import youtube_dl

def download_soundcloud_link(url, output_path='.', format='mp3', quality='192'):
    """
    Downloads a SoundCloud track given its URL.
    
    Parameters:
    - url (str): The SoundCloud track URL.
    - output_path (str): The path to save the downloaded track. Default is the current directory.
    - format (str): Desired audio format. Common formats include 'mp3', 'aac', 'flac', 'wav'. Default is 'mp3'.
    - quality (str): Desired audio bitrate for lossy formats like 'mp3'. Common values: '128', '192', '320'. Default is '192'.
    
    Note:
    - For most use-cases, 'mp3' format with '192kbps' offers a good balance between quality and file size.
    - For best quality, consider using '320kbps'. However, this will result in larger file sizes.
    """
    
    ydl_opts = {
        'format': 'bestaudio/best',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': format,
            'preferredquality': quality,
        }],
        'outtmpl': f"{output_path}/%(title)s.%(ext)s",
    }
    
    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])

    return f"{output_path}/{url.split('/')[-1]}.{format}"

def search_download_from_soundcloud(query, output_path='.', format='bestaudio/best',
                             extract_audio=True, audio_format='mp3', audio_quality='192k',
                             noplaylist=True, nocheckcertificate=True, quiet=False,
                             no_warnings=True, download_archive=None, source_address=None,
                             geo_bypass_country=None, socket_timeout=None, retries=10,
                             playlist_start=1, playlist_end=None, max_downloads=1):
    """
    Download audio from SoundCloud based on a search query.

    Parameters:
    - query (str): Search query for SoundCloud.
    - output_path (str): Directory for storing downloaded files. Defaults to current directory.
    - format (str): Desired format. Default is 'bestaudio/best'.
    - extract_audio (bool): Download only audio. Default is True.
    - audio_format (str): Desired audio format. Default is 'mp3'.
    - audio_quality (str): Desired audio quality. Default is '192k'.
    - noplaylist (bool): Download only video if URL refers to a video and playlist. Default is True.
    - nocheckcertificate (bool): Skip SSL certificate verification. Default is True.
    - quiet (bool): Enable quiet mode. Default is False.
    - no_warnings (bool): Ignore warnings. Default is True.
    - download_archive (str): File to record downloaded video IDs. Downloads only videos not listed in this file.
    - source_address (str): Client-side IP address to bind to.
    - geo_bypass_country (str): Bypass geographic restriction using given two-letter ISO 3166-2 country code.
    - socket_timeout (int): Timeout for socket operations.
    - retries (int): Number of retries for download. Default is 10.
    - playlist_start (int): Playlist video to start at. Default is 1.
    - playlist_end (int): Playlist video to end at.
    - max_downloads (int): Limit number of files to download.

    Returns:
    - None
    """
    
    # Ensure output directory exists
    if not os.path.exists(output_path):
        os.makedirs(output_path)
    
    outtmpl = os.path.join(output_path, '%(title)s.%(ext)s')

    postprocessors = [{
        'key': 'FFmpegExtractAudio',
        'preferredcodec': audio_format,
        'preferredquality': audio_quality,
    }]
    
    ydl_opts = {
        'format': format,
        'postprocessors': postprocessors,
        'extractaudio': extract_audio,
        'audioformat': audio_format,
        'audioquality': audio_quality,
        'noplaylist': noplaylist,
        'nocheckcertificate': nocheckcertificate,
        'quiet': quiet,
        'no_warnings': no_warnings,
        'outtmpl': outtmpl,
        'download_archive': download_archive,
        'source_address': source_address,
        'geo_bypass_country': geo_bypass_country,
        'socket_timeout': socket_timeout,
        'retries': retries,
        'playlist_start': playlist_start,
        'playlist_end': playlist_end,
        'max_downloads': max_downloads,
        'default_search': 'scsearch{}'.format(':' + str(max_downloads) if max_downloads else '') + ':'
    }

    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        ydl.download([query])

    # Return the path to the downloaded file
    return f"{output_path}/{query}.{audio_format}"



if __name__ == '__main__':
    
    #url = 'https://soundcloud.com/platform/hard-dance-040-trym'
    #download_soundcloud_link(url, output_path='/Users/nimamanaf/Desktop/Music/Trym')
    song_name = 'Funk Tribu - Blue Summer (Original Mix)'
    search_download_from_soundcloud(song_name, output_path='/Users/nimamanaf/Desktop/Music/Trym')
    
    