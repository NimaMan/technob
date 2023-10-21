
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.firefox.options import Options


def initialize_firefox_driver(headless=True):
    options = Options()
    if headless:
        options.add_argument('--headless')
    return webdriver.Firefox(options=options)


def initialize_chrome_driver(headless=True):
    options = Options()
    if headless:
        options.add_argument('--headless')
    return webdriver.Chrome(options=options)


def initialize_safari_driver():
    return webdriver.Safari()


def initialize_driver(driver_type='firefox', headless=True):
    if driver_type == 'firefox':
        return initialize_firefox_driver(headless=headless)
    elif driver_type == 'chrome':
        return initialize_chrome_driver(headless=headless)
    elif driver_type == 'safari':
        return initialize_safari_driver()
    else:
        raise ValueError(f"Unknown driver type: {driver_type}")

    