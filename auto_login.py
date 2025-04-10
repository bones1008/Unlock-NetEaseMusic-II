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
    #chrome_options.add_extension('NetEaseMusicWorldPlus.crx')

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
    browser.add_cookie({"name": "MUSIC_U", "value": "00BDB41ADD2E1EE4B42B729E178021896F108B4881C18CA741AA7BDD954DF213C89DD611537473635BC5064C9BC1D6745F2D4FAA5BA06C823B995B029A639BD01921AAFFC8594237B2B5C9D7AC705C39463CD6C60BFD478E52B966B34513ECD4C54CD1225F64A9480DDC7199D4B8B0DDA5855581A9E070667D0F28416F8FAE280F20D6105C73CF929EE078E4AF7DD2CEF1E6908F894B194495F5918F5155B3BEE82F0E89AC860185BC22B842448591BB7E01BF8DEFE8826F7CEF0A77DD8D7E0C4EAECBAE7BCEDD0ED6201E80B72F82BF8836CC6C703509AE8FD546AB1A67C6244E67AB8745CE241A4219BBA990300B4C23281D63105E68879DADD7CB8E9503ED7FCF67AA138E14BF80A172D1C2FCEB76E4D98E578DC41B3597D36A24B2738224AB81A9DE579EA2DBEEF82A7F294DB57CBF86A3B47E8B89C12211F223CA6CE905DA77FCD2D7CC964D0B35DE8D2C4A970A40363B29E638AEA976BBCB7C5F4EA56AD4"})
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
