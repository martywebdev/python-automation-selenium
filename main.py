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

load_dotenv()

USERNAME = os.getenv("APP_USERNAME")
PASSWORD = os.getenv("APP_PASSWORD")
CHROMEDRIVER_PATH = os.getenv(
    "CHROMEDRIVER_PATH", "chromedriver-win64/chromedriver.exe")
WAIT_SECONDS = int(os.getenv("WAIT_SECONDS", "10"))

if not USERNAME or not PASSWORD:
    print("ERROR: APP_USERNAME and APP_PASSWORD must be set in .env")
    sys.exit(1)


def create_driver(chromedriver_path: str = CHROMEDRIVER_PATH):
    options = Options()
    options.add_argument("--disable-search-engine-choice-screen")
    # options.add_argument("--start-maximized")  # optional for debugging
    service = Service(chromedriver_path)
    return webdriver.Chrome(service=service, options=options)


def safe_click(driver, element, wait: WebDriverWait = None):
    """Try scroll -> normal click -> fallback to JS click if blocked."""
    try:
        driver.execute_script(
            "arguments[0].scrollIntoView({block: 'center'});", element)
        element.click()
    except ElementClickInterceptedException:
        # try waiting until clickable then click again
        if wait:
            try:
                # no-op; we already have element
                wait.until(EC.element_to_be_clickable((By.XPATH, ".")))
            except Exception:
                pass
        # fallback: JS click
        driver.execute_script("arguments[0].click();", element)


def login(driver):
    driver.get("https://demoqa.com/login")
    wait = WebDriverWait(driver, WAIT_SECONDS)

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

    safe_click(driver, login_btn, wait=wait)


def fill_text_box_form(driver):
    wait = WebDriverWait(driver, WAIT_SECONDS)

    try:
        # avoid brittle absolute XPaths; prefer a shorter relative one if possible
        elements_panel = wait.until(EC.element_to_be_clickable(
            # example selector; adjust to actual site
            (By.CSS_SELECTOR, "div.element-group")))
        elements_panel.click()

        text_box_item = wait.until(
            EC.element_to_be_clickable((By.ID, "item-0")))
        # text_box_item.click()

        driver.execute_script(
            "arguments[0].click()", text_box_item)

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

    safe_click(driver, submit_btn, wait=wait)

    # x = driver.find_elements(By.CSS_SELECTOR, 'div.element-group')
    # x[1].click()


def download(driver):
    wait = WebDriverWait(driver, WAIT_SECONDS)

    try:

        elements_group = driver.find_elements(
            By.CSS_SELECTOR, 'div.element-group')

        elements_group[0].click()

        links = wait.until(EC.visibility_of_element_located((By.ID, 'item-7')))

        links.click()

        download_button = wait.until(
            EC.visibility_of_element_located((By.ID, 'downloadButton')))

        download_button.click()

    except TimeoutException as exc:
        raise RuntimeError("Form elements not found (timeout)") from exc


if __name__ == "__main__":
    driver = create_driver()
    try:
        login(driver)
        fill_text_box_form(driver)
        download(driver)
        input("Press enter to close the browser")
    finally:
        driver.quit()
