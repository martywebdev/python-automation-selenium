import os
import sys
from dotenv import load_dotenv
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException, ElementClickInterceptedException


# ==============================
# Setup
# ==============================

load_dotenv()

USERNAME = os.getenv("APP_USERNAME")
PASSWORD = os.getenv("APP_PASSWORD")
CHROMEDRIVER_PATH = os.getenv(
    "CHROMEDRIVER_PATH", "chromedriver-win64/chromedriver.exe")
WAIT_SECONDS = int(os.getenv("WAIT_SECONDS", "10"))

if not USERNAME or not PASSWORD:
    print("ERROR: APP_USERNAME and APP_PASSWORD must be set in .env")
    sys.exit(1)


# ==============================
# Driver / Utilities
# ==============================

def create_driver(download_subdir: str="downloads"):
    options = Options()
    options.add_argument("--disable-search-engine-choice-screen")

      # create subfolder inside CWD
    download_path = os.path.join(os.getcwd(), download_subdir)
    os.makedirs(download_path, exist_ok=True)

    prefs = {
        "download.default_directory": download_path,
        "download.prompt_for_download": False,      # no popup
        "download.directory_upgrade": True,         # overwrite old settings
        "safebrowsing.enabled": True                # avoid Chrome blocking .exe/.zip
    }
    options.add_experimental_option('prefs', prefs)

    service = Service(CHROMEDRIVER_PATH)
    
    return webdriver.Chrome(service=service, options=options)


def safe_click(driver, element):
    """Scroll into view → normal click → fallback JS click if blocked."""
    try:
        driver.execute_script(
            "arguments[0].scrollIntoView({block: 'center'});", element)
        element.click()
    except ElementClickInterceptedException:
        driver.execute_script("arguments[0].click();", element)


# ==============================
# Workflows
# ==============================

def login(driver):
    wait = WebDriverWait(driver, WAIT_SECONDS)
    driver.get("https://demoqa.com/login")

    try:
        user_field = wait.until(
            EC.visibility_of_element_located((By.ID, "userName")))
        pass_field = wait.until(
            EC.visibility_of_element_located((By.ID, "password")))
        login_btn = wait.until(EC.element_to_be_clickable((By.ID, "login")))
    except TimeoutException as exc:
        raise RuntimeError("Login page elements not found (timeout)") from exc

    user_field.clear()
    user_field.send_keys(USERNAME)
    pass_field.clear()
    pass_field.send_keys(PASSWORD)

    safe_click(driver, login_btn)


def fill_text_box_form(driver):
    wait = WebDriverWait(driver, WAIT_SECONDS)

    try:
        elements_panel = wait.until(EC.element_to_be_clickable(
            (By.CSS_SELECTOR, "div.element-group")))
        elements_panel.click()

        text_box_item = wait.until(
            EC.element_to_be_clickable((By.ID, "item-0")))
        safe_click(driver, text_box_item)

        fullname_field = wait.until(
            EC.visibility_of_element_located((By.ID, "userName")))
        email_field = wait.until(
            EC.visibility_of_element_located((By.ID, "userEmail")))
        current_address_field = wait.until(
            EC.visibility_of_element_located((By.ID, "currentAddress")))
        permanent_address_field = wait.until(
            EC.visibility_of_element_located((By.ID, "permanentAddress")))
        submit_btn = wait.until(EC.element_to_be_clickable((By.ID, "submit")))
    except TimeoutException as exc:
        raise RuntimeError("Form elements not found (timeout)") from exc

    fullname_field.clear()
    fullname_field.send_keys("John Smith")
    email_field.clear()
    email_field.send_keys("john@gmail.com")
    current_address_field.clear()
    current_address_field.send_keys("Matatag Street Pinyahan Quezon city")
    permanent_address_field.clear()
    permanent_address_field.send_keys("Matatag Street Pinyahan Quezon city")

    safe_click(driver, submit_btn)


def download_file(driver):
    wait = WebDriverWait(driver, WAIT_SECONDS)

    try:
        elements_group = driver.find_elements(
            By.CSS_SELECTOR, 'div.element-group')
        elements_group[0].click()  # first group only

        links = wait.until(EC.element_to_be_clickable((By.ID, 'item-7')))
        safe_click(driver, links)

        download_button = wait.until(
            EC.element_to_be_clickable((By.ID, 'downloadButton')))
        safe_click(driver, download_button)

    except TimeoutException as exc:
        raise RuntimeError("Download elements not found (timeout)") from exc


# ==============================
# Main
# ==============================

if __name__ == "__main__":
    driver = create_driver("my_files")
    try:
        login(driver)
        fill_text_box_form(driver)   # comment this out if not needed
        download_file(driver)        # comment this out if not needed
        input("Press Enter to close the browser...")
    finally:
        driver.quit()
