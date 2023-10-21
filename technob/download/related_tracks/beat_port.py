# %%
import os 
import re
import pandas as pd
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import StaleElementReferenceException
from selenium.webdriver.support import expected_conditions as EC
from technob.download.scrapping.utils import initialize_driver


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
    print(len(song_chunks))
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
            else:  # added this else block to handle cases where BPM and Key aren't split
                song_info.insert(5, "Unknown Key")  # adding a placeholder for Key if it's not available
            song_data.append(song_info)
    ''' This is the working one
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
    '''
    #print(song_data)
    # Create a pandas DataFrame
    columns = ['Song', 'Artist', 'Label', 'Genre', 'BPM', 'BP Key', 'Release Date', 'Price']
    df = pd.DataFrame(song_data, columns=columns)
    
    return df




def get_related_tracks_from_raw_text(url):
    driver = initialize_driver()
    # Navigate to the URL
    driver.get(url)
    # Relocate the element and then interact with it
    try:
        # Wait for the element to be present
        wait = WebDriverWait(driver, 10)
        element = wait.until(
            EC.presence_of_element_located((By.CSS_SELECTOR, ".sc-fdd08fbd-2.gwqVZO"))
        )
        element_text = element.text
    
    except Exception as e:
        element_text = ''
        print(f'Error: {e}')

    finally:
        # Don't forget to close the driver
        driver.quit()
        # remove the log file 
        os.remove('geckodriver.log')
        return element_text



def extract_related_tracks(element):
        # Extract the song link
        # Extract the release link
        #release_link_element = element.find_element(By.CSS_SELECTOR, '.sc-b26882fe-5.eWVvdf a.artwork')
        #release_link = release_link_element.get_attribute('href')

        # Extract the track link
        song_link_element = element.find_element(By.CSS_SELECTOR, '.sc-fdd08fbd-0.bgDQwW.cell.title .container a')
        song_link = song_link_element.get_attribute('href')

        # Extract other information
        song_title_element = element.find_element(By.CSS_SELECTOR, '.container a span')
        song_title = song_title_element.text
        
        artist_element = element.find_element(By.CSS_SELECTOR, '.container .sc-c3b4898e-0')
        artist = artist_element.text
        
        label_element = element.find_element(By.CSS_SELECTOR, '.cell.label a')
        label = label_element.text
        
        genre_element = element.find_element(By.CSS_SELECTOR, '.cell.bpm a')
        genre = genre_element.text
        
        bpm_key_element = element.find_element(By.CSS_SELECTOR, '.cell.bpm div')
        bpm_key_text = bpm_key_element.text
        bpm, key = bpm_key_text.split(' - ')
        
        release_date_element = element.find_element(By.CSS_SELECTOR, '.cell.date')
        release_date = release_date_element.text
        
        price_element = element.find_element(By.CSS_SELECTOR, '.cell.card .price')
        price = price_element.text
        
        song_info = [song_title, artist, label, genre, bpm, key, release_date, price, song_link]
        return song_info


def get_related_tracks(url, headless=True, driver_type='firefox',  max_retries=5):
    # Get the raw text
    driver = initialize_driver(headless=headless, driver_type=driver_type)
    # Navigate to the URL
    driver.get(url) 
    try:
        # Wait for the element to be present
        wait = WebDriverWait(driver, 10)
        recom_songs = wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, ".sc-fdd08fbd-1.gwklwO.row")))
        #recom_df = extract_related_tracks(recom_songs) 
        song_data = []
        i = 0
        retries = 0
       
        while i < len(recom_songs) and retries < max_retries:
            try:        
                element = driver.find_elements(By.CSS_SELECTOR, ".sc-fdd08fbd-1.gwklwO.row")[i]
                song_info = extract_related_tracks(element)
                song_data.append(song_info)
                i += 1  # Move on to the next element
                retries = 0  # Reset the retries counter as we successfully processed this element
            except StaleElementReferenceException:
                retries += 1  # Increment the retries counter
                continue  # Retry the current element
    
        # Create a pandas DataFrame
        columns = ['Song', 'Artist', 'Label', 'Genre', 'BPM', 'BP Key', 'Release Date', 'Price', 'URL']
        recom_df = pd.DataFrame(song_data, columns=columns)
    
    except Exception as e:
        recom_df = pd.DataFrame()
        print(f'Error: {e}')
    finally:
        # Don't forget to close the driver
        driver.quit()
        # remove the log file 
        os.remove('geckodriver.log')
        return recom_df


if __name__ == '__main__':
    url = 'https://www.beatport.com/track/one-time/18171709'
    # Now song_info_list should contain the song info from the webpage

    df = get_related_tracks(url)
    #df.to_csv('beatport_temp.csv', index=False)
    print(df.head())
# %%
