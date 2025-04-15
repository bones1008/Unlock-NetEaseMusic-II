# coding: utf-8

import os
import time
import logging
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from retrying import retry

from selenium.webdriver.chrome.options import Options

chrome_options = Options()

# Make Chrome look more real
chrome_options.add_argument('--disable-blink-features=AutomationControlled')

# Remove automation notice in navigator.webdriver
chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
chrome_options.add_experimental_option('useAutomationExtension', False)

service = Service(ChromeDriverManager().install())
browser = webdriver.Chrome(service=service, options=chrome_options)

# Configure logging
logging.basicConfig(level=logging.INFO, format='[%(levelname)s] %(asctime)s %(message)s')

@retry(wait_random_min=5000, wait_random_max=10000, stop_max_attempt_number=3)
def enter_iframe(browser):
    logging.info("Enter login iframe")
    time.sleep(5)  # 给 iframe 额外时间加载
    try:
        iframe = WebDriverWait(browser, 10).until(
            EC.presence_of_element_located((By.XPATH, "//*[starts-with(@id,'x-URS-iframe')]")
        ))
        browser.switch_to.frame(iframe)
        logging.info("Switched to login iframe")
    except Exception as e:
        logging.error(f"Failed to enter iframe: {e}")
        browser.save_screenshot("debug_iframe.png")  # 记录截图
        raise
    return browser

@retry(wait_random_min=1000, wait_random_max=3000, stop_max_attempt_number=5)
def extension_login():
    chrome_options = webdriver.ChromeOptions()

    logging.info("Load Chrome extension NetEaseMusicWorldPlus")
    chrome_options.add_extension('NetEaseMusicWorldPlus.crx')

    logging.info("Initializing Chrome WebDriver")
    try:
        service = Service(ChromeDriverManager().install())  # Auto-download correct chromedriver
        browser = webdriver.Chrome(service=service, options=chrome_options)
    except Exception as e:
        logging.error(f"Failed to initialize ChromeDriver: {e}")
        return

    # Set global implicit wait
    browser.implicitly_wait(20)

    browser.get('https://music.163.com')

    # Inject Cookie to skip login
    logging.info("Injecting Cookie to skip login")
    browser.add_cookie({"name": "MUSIC_U", "value": "00A3F70C074FAA12CE7C125FFEBC7B06F8806991BA08E5C8FC221E8C29B57A5633F28A16DEC616C74A8EDEC830D8FAB0750806848BAAF79B330C89071E9903C3CB4E0C448B039AA3753895D41C73A0A288630D515870DB341142E053FF7302AEE32B1B6C463C903CD32A25C5BB0D23B44F0327E609EC90F4A5C69891DFA18DE5683C7B6E0B5BDEDC44651AF53CD8B2F3F5BEC04A4E7A9F7E1A54C6ECF24A0C43D1EDB59DA9CE3B339D5C803CAEB01839EF8C59456AE7BC253B78B9C44AE6B42F2628DC3F55BAF52BA4BB837E052C65A79C10FFBE8D58B56BF67614D510423AEEE3C79563948928B5B8F5313C4B961A4D9F9B426A10395A8555891794D61141AAEA51CA97AA501266EFE05B90B2CAAF71C37A540E7258F4072424A8DFF5C7D14856B5CFCF09111330946442B9996B1ACF3638ED0D5CE3601918B5034E5D6D83C92105A4EFE40D8439F9F9AE76C79848821BBA6FEF1410F250F09F08E6C4682A3ECB"})
    browser.refresh()
    time.sleep(5)
    
    # Save screenshot and HTML for debugging
    browser.save_screenshot("debug_output.png")
    with open("page.html", "w", encoding="utf-8") as f:
        f.write(browser.page_source)
    
    print("Saved page state for debugging.")

    time.sleep(5)  # Wait for the page to refresh
    logging.info("Cookie login successful")

    # Confirm login is successful
    logging.info("Unlock finished")

    time.sleep(10)
    browser.quit()


if __name__ == '__main__':
    try:
        extension_login()
    except Exception as e:
        logging.error(f"Failed to execute login script: {e}")
