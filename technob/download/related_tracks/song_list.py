
# %%
import os 
import pandas as pd
import numpy as np
from technob.download.related_tracks.beat_port import get_related_tracks


def getsong_list(url, page=1, per_page=150,  max_page=67):
    
    url = f"{url}?page={page}&per_page={per_page}"
    df_db = get_related_tracks(url)
    error_pages = []  # list to keep track of pages that cause an error

    for page in range(2, max_page+1):
        try:
            url = f"https://www.beatport.com/genre/hard-techno/2/tracks?page={page}&per_page=150"
            df = get_related_tracks(url)
            df_db = pd.concat([df_db, df], ignore_index=True)
        except Exception as e:  # it's a good practice to catch specific exceptions
            print(f"Error at page {page}: {e}")
            error_pages.append(page)  # append the page number to the error_pages list
            continue
    
    print(f"Number of remaining pages: {len(error_pages)}")
    while error_pages:  # continue as long as there are error pages
        # choose a first at random
        idx = np.random.randint(0, len(error_pages))
        page = error_pages.pop(idx)  # remove the page number from error_pages
        try:
            url = f"https://www.beatport.com/genre/hard-techno/2/tracks?page={page}&per_page=150"
            df = get_related_tracks(url)
            df_db = pd.concat([df_db, df], ignore_index=True)
        except Exception as e:
            print(f"Error at page {page}: {e}")
            error_pages.append(page)  # re-append the page number to error_pages if error occurs again
            continue  # skip to the next iteration
    
    return df_db


bp_genres = {'melodic-house-techno': "https://www.beatport.com/genre/melodic-house-techno/90/tracks",
             'minimal-deep-tech': "https://www.beatport.com/genre/minimal-deep-tech/14/tracks",
            'nu-disco-disco': "https://www.beatport.com/genre/nu-disco-disco/50/tracks",
            'progressive-house': "https://www.beatport.com/genre/progressive-house/15/tracks",
            'tech-house': "https://www.beatport.com/genre/tech-house/11/tracks",
            'py-trance': "https://www.beatport.com/genre/psy-trance/13/tracks",
            'hard-dance-hardcore':'https://www.beatport.com/genre/hard-dance-hardcore/8',
            'funky-house': "https://www.beatport.com/genre/funky-house/81",
            'house': 'https://www.beatport.com/genre/house/5/tracks',
            'melodic-house-techno': 'https://www.beatport.com/genre/melodic-house-techno/90/tracks',
            'techno': "https://www.beatport.com/genre/techno/6/tracks",
            'hard-techno': "https://www.beatport.com/genre/hard-techno/2/tracks",
            'house-deep-house': "https://www.beatport.com/genre/house-deep-house/12/tracks",
            'electronica': 'https://www.beatport.com/genre/electronica/3/tracks',
            'techno-peak-time-driving': "https://www.beatport.com/genre/techno-peak-time-driving/6/tracks",
            'techno-raw-deep-hypnotic': "https://www.beatport.com/genre/techno-raw-deep-hypnotic/92/tracks",
            'techno-detroit': "https://www.beatport.com/genre/techno-detroit/18/tracks",
            'techno-hard': "https://www.beatport.com/genre/techno-hard/5/tracks",
            'techno-minimal': "https://www.beatport.com/genre/techno-minimal/14/tracks",
            'techno-dub': "https://www.beatport.com/genre/techno-dub/92/tracks",
            'techno-experimental': "https://www.beatport.com/genre/techno-experimental/92/tracks",
            'techno-industrial': "https://www.beatport.com/genre/techno-industrial/92/tracks",
            'techno-melodic': "https://www.beatport.com/genre/techno-melodic/92/tracks",
            'techno-organic': "https://www.beatport.com/genre/techno-organic/92/tracks",
            'techno-tribal': "https://www.beatport.com/genre/techno-tribal/92/tracks",
            'techno-trance': "https://www.beatport.com/genre/techno-trance/92/tracks",
            'techno-uk-jackin': "https://www.beatport.com/genre/techno-uk-jackin/92/tracks",
            'electro-classic-detroit-modern': 'https://www.beatport.com/genre/electro-classic-detroit-modern/94/tracks',
            'electro-breaks': 'https://www.beatport.com/genre/electro-breaks/94/tracks',
            'electro': 'https://www.beatport.com/genre/electro/94/tracks',
            'breaks': 'https://www.beatport.com/genre/breaks/9/tracks',
            'breaks-psy-trance': 'https://www.beatport.com/genre/breaks-psy-trance/9/tracks',
            'breaks-tech': 'https://www.beatport.com/genre/breaks-tech/9/tracks',
            'breaks': 'https://www.beatport.com/genre/breaks/9/tracks',
            'breaks-psy-trance': 'https://www.beatport.com/genre/breaks-psy-trance/9/tracks',
            'breaks-tech': 'https://www.beatport.com/genre/breaks-tech/9/tracks',
            'breaks': 'https://www.beatport.com/genre/breaks/9/tracks',

            
             }
    
if __name__ == '__main__':
    
    genre = "house"
    url = bp_genres[genre]
    df_db = getsong_list(url, page=1, per_page=150,  max_page=67)
    
    output_path = "/Users/nimamanaf/Library/CloudStorage/GoogleDrive-ndizbin14@ku.edu.tr/My Drive/Techno/technob/data"
    df_db.to_csv(os.path.join(output_path, f"{genre}.csv"), index=False)