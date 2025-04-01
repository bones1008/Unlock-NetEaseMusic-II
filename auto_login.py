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
    browser.add_cookie({"name": "MUSIC_U", "value": "007D4BBBFECBDA06A3658C77F5AEB5802CC8F27FD1B2B725766DD330DBF9A94DAEDA3D616097ECB1CDC4D0BE8263824BACA369A3581ACD34DD7DB5EFD0FF7998B00D680A799DEA3A9E5E2CB9DFFBB9388247E78C2EA44062E5F4F3BA94F23BD5C8F4CC4AF9151710DC4BC6E2E96DA6D53350B96D5D5EE761256D220D05089CB4DCB39832CD978FECFD3D7C5FCF665B9371365F951C3ED4CFBA5DB20000F46EBF3DE70BA3C61B8933AF87318850608C05D2246C232838868E4167651F063AA7F154C84913069B6E39A6AABD0843E467164805C3913DA5079AD8C91BE7A49EDE7C87B72BE1F6926051126D5046DF230423AF356C49D166442315DFEAA72AC0DF21FDCC2C84DD7A883E7189C90C33351151978C92EDB4DF3809E4D6E713133C56FA8EE2E2B782D546D9324C8E9FF4C03F30A357D8E9EF3111847BD8DBBCABE8CBA03C1697429E45D9D56110FE59EB1A4CE60514BF922269D6CFA0670D28833B513880"})
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
