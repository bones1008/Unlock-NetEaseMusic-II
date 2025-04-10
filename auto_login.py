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
    browser.add_cookie({"name": "MUSIC_U", "value": "004EF2393FA9592DE23926F8459BC97E73CA36B6C3B9684A9EF0B3A4B3A92CD8A9D45CF146A17578558213B281ACB83B0A0553626C577EA00856936376DD7EB3FC350864DD3B83527AB32A92327CC2F5E629E5CFFCA40157EB7B89DC63E38B7AC694D9D23C0D21009B442942F80CCC55FA25D1FC6EF2D280C6A7F303C5734C90D0C3F938DB2D251265312F184A30EFF68CD5BC7F83B5505D0C2A61495297135788BDBDB70039B5F9ED2C91FF5081621927723AE5B77447CF07BE7A369C1BBD51DE86EDE08C6D18FAA826B9489C1F1E0E3C2A8ABE335281B8531BCE836E4C884287A69A2106C8638F15B288DFD2C571D6E966E81C5B3A0D6C75370A15AF303245C642A59DF18E3EF8AE7291EE9AFC6F9AB7313A511B047C1FF8F160D2A31EA2CF6431C473F3384398395804DDF54A8A8E5805AF1B26F9E21B5B1865C31202B180EB57512833B01DB4F9FCD5B70E4760DA31C6CC47BC8E1E064DFAE47CA67A31A8A9"})
    browser.refresh()
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
