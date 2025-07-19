import undetected_chromedriver as uc
import os
import stat
import tempfile
import time
from selenium.webdriver.common.by import By

# Paths to Chrome binary and Chromedriver
CHROME_BINARY = r"C:\Users\abhay\Downloads\chrome-win64\chrome-win64\chrome.exe"
CHROMEDRIVER_SRC = r"C:\Users\abhay\Downloads\chromedriver-win64\chromedriver-win64\chromedriver.exe"

def patch_and_get_driver_path():
    """Copy chromedriver to a temp location and make it executable."""
    dst_fd, dst_path = tempfile.mkstemp(suffix=".exe")
    with open(CHROMEDRIVER_SRC, "rb") as src_f, open(dst_fd, "wb") as dst_f:
        dst_f.write(src_f.read())
    os.chmod(dst_path, stat.S_IWRITE | stat.S_IREAD | stat.S_IEXEC)
    return dst_path

def launch_browser_for_user(user: str):
    """Launch a Chrome instance for a specific user with their profile directory."""
    user_profile_dir = rf"C:\Users\abhay\Desktop\bots\profiles\{user.lower()}"

    # Ensure the profile directory exists
    os.makedirs(user_profile_dir, exist_ok=True)

    # Set up Chrome options
    options = uc.ChromeOptions()
    options.binary_location = CHROME_BINARY
    options.add_argument(f"--user-data-dir={user_profile_dir}")
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_argument("--disable-infobars")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--no-sandbox")
    options.add_argument("--start-maximized")
    options.add_argument("--disable-gpu")
    options.add_argument("--disable-extensions")

    # Launch Chrome with undetected_chromedriver
    driver_path = patch_and_get_driver_path()
    driver = uc.Chrome(
        driver_executable_path=driver_path,
        version_main=137,  # Ensure this matches your Chrome version, or remove if auto-detection works
        options=options
    )
    return driver

import time

def open_core_tabs(driver):
    driver.get("https://chat.openai.com")
    print(f"Tab 0 handle: {driver.current_window_handle}")
    time.sleep(2)

    driver.switch_to.new_window('tab')
    print(f"Tab 1 handle: {driver.current_window_handle}")
    driver.get("https://www.linkedin.com/feed/")
    time.sleep(2)

    driver.switch_to.new_window('tab')
    print(f"Tab 2 handle: {driver.current_window_handle}")
    driver.get("https://twitter.com/home")
    time.sleep(2)

    driver.switch_to.window(driver.window_handles[0])
    print(f"Back to Tab 0 handle: {driver.current_window_handle}")