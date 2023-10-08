# %%
import os 
import re
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.firefox.options import Options

def process_song_info(text_data):
    # Remove "Exclusive" at the beginning of lines
    text_data = text_data.replace('\nExclusive', '')
    text_data = text_data.replace('Exclusive', '')
    
    # Use regex to split text by lines starting with a number and newline
    #song_chunks = re.split(r'\n(?=\d+\n)', text_data)
    song_chunks = re.split(r'\n(?=\d+\n[^\n]+)', text_data)
    
    if song_chunks[0] == '':
        song_chunks = song_chunks[1:]
    # Process each chunk separately
    for idx, chunk in enumerate(song_chunks):
        lines = chunk.strip().split('\n')
        if idx == len(song_chunks)-1:
            song_chunks[idx] = lines
            continue
        if len(lines) < 7:
            next_line = song_chunks[idx+1].strip().split('\n')
            if ((len(next_line) + len(lines)) == 8) or ((len(next_line) + len(lines)) == 9):
                # combine the two chunks together
                lines = lines + next_line
                song_chunks[idx] = lines
                # remove the next chunk
                song_chunks.pop(idx+1)
                #print(idx, lines)
        else:
            song_chunks[idx] = lines
            #print(idx, lines)

    # Initialize an empty list to hold song data
    song_data = []
    # Process each chunk separately
    for idx, lines in enumerate(song_chunks):
        # Ensure there are at least 7 lines of data (some chunks might be empty)
        if len(lines) >= 7:
            song_info = lines[1:8]  # Exclude the track number
            # Split BPM and key
            bpm_key = song_info[4].split(' - ')
            if len(bpm_key) == 2:
                song_info[4] = bpm_key[0]  # BPM
                song_info.insert(5, bpm_key[1])  # Key
            song_data.append(song_info)
    
    # Create a pandas DataFrame
    columns = ['Title', 'Artist', 'Label', 'Genre', 'BPM', 'Key', 'Release Date', 'Price']
    df = pd.DataFrame(song_data, columns=columns)
    
    return df


def initialize_driver():
    options = Options()
    options.add_argument('--headless')
    return webdriver.Firefox(options=options)


def get_related_tracks_raw(url):
    driver = initialize_driver()
    # Navigate to the URL
    driver.get(url)
    # Relocate the element and then interact with it
    try:
        # Wait for the element to be present
        element = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, ".sc-fdd08fbd-2.gwqVZO"))
        )
        
        # Interact with the element immediately after locating
        element_text = element.text
        #print(f'Text of the element: {element_text}')
    except Exception as e:
        element_text = ''
        print(f'Error: {e}')

    finally:
        # Don't forget to close the driver
        driver.quit()
        # remove the log file 
        os.remove('geckodriver.log')
        return element_text


def get_related_tracks(url):
    # Get the raw text
    raw_text = get_related_tracks_raw(url)
    # Process the raw text
    df = process_song_info(raw_text)
    return df


if __name__ == '__main__':
    url = 'https://www.beatport.com/track/one-time/18171709'
    df = get_related_tracks(url)
    df.to_csv('beatport_temp.csv', index=False)