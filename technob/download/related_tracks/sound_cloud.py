# %%
# %%
import os
from datetime import datetime
import pandas as pd
import traceback
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.firefox.options import Options
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from urllib3.exceptions import MaxRetryError


def fetch_soundcloud_data(song_url_or_name, driver):
    """
    Fetch song details from a given SoundCloud URL or search query.
    """
    if not isinstance(song_url_or_name, str):
        return pd.DataFrame()
    # Ensure the URL ends with /recommended
    if not song_url_or_name.endswith("/recommended"):
        song_url_or_name += "/recommended"

    try:
        # Navigate to the song URL
        driver.get(song_url_or_name if song_url_or_name.startswith('http') else f"https://soundcloud.com/search?q={song_url_or_name}")

        # Wait for the content to load
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, "soundList__item")))
        song_item = driver.find_elements(By.CLASS_NAME, "soundList__item")
        # Initialize list to store song details
        songs = []

        # Fetch and store details of each song
        for song_item in song_item:
            song_details = {}
            # Extract individual fields and handle exceptions
            for field, (css_selector, default) in {
                'Song': (".sc-link-primary.soundTitle__title", " "),
                'Artist': (".soundTitle__usernameText", " "),
                'Genre': (".sc-tagContent", " "),
                'Reposts': (".sc-button-repost", " "),
                'Comments': (".sc-ministats-comments", " "),
                'Sound_Cloud_Link': (".sound__coverArt", " "),
            }.items():
                try:
                    song_details[field] = song_item.find_element(By.CSS_SELECTOR, css_selector).text if field != 'Comments' else song_item.find_element(By.CSS_SELECTOR, css_selector).text.split("\n")[1] if "\n" in song_item.find_element(By.CSS_SELECTOR, css_selector).text else '0'
                except NoSuchElementException:
                    song_details[field] = default

            # Special handling for 'Likes' due to its complexity
            try:
                num_likes = song_item.find_element(By.CSS_SELECTOR, ".sc-button-like").text
                song_details['Likes'] = int(float(num_likes.replace("K", "").replace(",", "")) * 1000 if "K" in num_likes else num_likes)
            except Exception:
                song_details['Likes'] = 0  # Set default as 0

            # Add more details and append to list
            song_details['Snatched_on'] = datetime.now().strftime('%Y-%m-%d')
            songs.append(song_details)

        # Convert list of song details to DataFrame
        return pd.DataFrame(songs)

    except Exception as e:
        print(f"Exception occurred: {e}")
        return pd.DataFrame()  # Return empty DataFrame if something fails


# Initialize the WebDriver with headless options
def initialize_driver():
    options = Options()
    options.add_argument('--headless')
    return webdriver.Firefox(options=options)


def main(initial_song=None, song_db_path="song_db.csv", max_num_songs=4000, verbose=False):
    try:
        song_db = pd.read_csv(song_db_path)
    except FileNotFoundError:
        song_db = pd.DataFrame(columns=["Song", "Artist", "Genre", "Likes", "Reposts", "Comments", "Sound_Cloud_Link", "SCUpload_Time", "Snatched_on"])
    song_db['Likes'] = song_db['Likes'].apply(pd.to_numeric, errors='coerce').fillna(0).astype(int)

    driver = initialize_driver()

    num_scraped_songs = 0
    scrapped_songs = set()
    iteration_count = 0  # Added counter for WebDriver restart

    try:
        while len(song_db) < max_num_songs:
            iteration_count += 1
            if iteration_count % 100 == 0:  # Restart WebDriver every 100 iterations
                driver.quit()
                driver = initialize_driver()

            # Choose what song to scrape next 
            if initial_song is not None and iteration_count == 1:
                current_song = initial_song
                current_song_name = initial_song.split("/")[-1]
            else:
                # random with a wieghted probability
                random_song = song_db.sample(weights="Likes").iloc[0]
                current_song_name = random_song["Song"]
                current_song = random_song["Sound_Cloud_Link"]
            if current_song in scrapped_songs:
                # choose another song randomly based on the number of likes
                current_song = song_db.sample().iloc[0]
                current_song_name = current_song["Song"]
                current_song = current_song["Sound_Cloud_Link"]
            if verbose:
                print(f"iteration {iteration_count} current song: {current_song_name}")
            retried_urls = set()
            # Initialize a variable to track retries
            retry_count = 0
            max_retries = 5  # Maximum number of retries
            try:
                # two cases: if we have gotten the related tracks one time, we can skip it or get it again
                if current_song not in retried_urls or retry_count < max_retries:
                    song_data_df = fetch_soundcloud_data(current_song, driver,)
                    if not song_data_df.empty:
                        song_db = pd.concat([song_db, song_data_df], ignore_index=True)
                        if verbose:
                            print(f"iteration {iteration_count} songs in the database: {len(song_db)}, scraped: {num_scraped_songs}, song_df: {len(song_data_df)}")
                    
                    # drop duplicates
                    song_db.drop_duplicates(subset=["Song", "Artist"], inplace=True)
                    # save the database
                    song_db.to_csv(song_db_path, index=False)
                    scrapped_songs.add(current_song)
                    num_scraped_songs = len(scrapped_songs)

                    retried_urls.add(current_song)
                    retry_count = 0  # Reset retry count if successful
                else:
                    print(f"skipping {current_song_name} with {retry_count} retries")

            except (TimeoutException, ConnectionRefusedError, MaxRetryError):
                print("Exception occurred. Restarting WebDriver.")
                driver.quit()
                driver = initialize_driver()
            except Exception as e:
                print("Unknown exception occurred. Details:")
                traceback.print_exc()
    finally:
        driver.quit()

    # sort the database by likes and comments
    song_db.sort_values(by=["Likes", "Comments"], ascending=False, inplace=True)
    song_db.reset_index(drop=True, inplace=True)
    song_db.to_csv(song_db_path, index=False)
    return song_db


if __name__ == "__main__":
    
    song = {"name": "init",  "url": "https://soundcloud.com/jayronmusic/jayron-karashnikov-gewoonraves-move-it"}
    db_path = "/Users/nimamanaf/Library/CloudStorage/OneDrive-KocUniversitesi/ses/techno"
    df_db = main(song["url"], song_db_path=os.path.join(db_path, "sc_db.csv"), verbose=True)
