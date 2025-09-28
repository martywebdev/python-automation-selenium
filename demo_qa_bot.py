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
# Config
# ==============================

load_dotenv()

USERNAME = os.getenv("APP_USERNAME")
PASSWORD = os.getenv("APP_PASSWORD")
CHROMEDRIVER_PATH = os.getenv("CHROMEDRIVER_PATH", "chromedriver-win64/chromedriver.exe")
WAIT_SECONDS = int(os.getenv("WAIT_SECONDS", "10"))

if not USERNAME or not PASSWORD:
    print("ERROR: APP_USERNAME and APP_PASSWORD must be set in .env")
    sys.exit(1)


# ==============================
# Page Bot Class
# ==============================

class DemoQABot:
    def __init__(self, username: str, password: str, driver_path: str = CHROMEDRIVER_PATH, wait_seconds: int = WAIT_SECONDS):
        self.username = username
        self.password = password
        self.wait_seconds = wait_seconds
        self.driver = self._create_driver(driver_path)
        self.wait = WebDriverWait(self.driver, wait_seconds)

    def _create_driver(self, path: str):
        options = Options()
        options.add_argument("--disable-search-engine-choice-screen")
        service = Service(path)
        return webdriver.Chrome(service=service, options=options)

    def safe_click(self, element):
        """Scroll into view → normal click → fallback JS click if blocked."""
        try:
            self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", element)
            element.click()
        except ElementClickInterceptedException:
            self.driver.execute_script("arguments[0].click();", element)

    # ------------------------------
    # Workflows
    # ------------------------------

    def login(self):
        self.driver.get("https://demoqa.com/login")

        try:
            user_field = self.wait.until(EC.visibility_of_element_located((By.ID, "userName")))
            pass_field = self.wait.until(EC.visibility_of_element_located((By.ID, "password")))
            login_btn = self.wait.until(EC.element_to_be_clickable((By.ID, "login")))
        except TimeoutException as exc:
            raise RuntimeError("Login page elements not found (timeout)") from exc

        user_field.clear()
        user_field.send_keys(self.username)
        pass_field.clear()
        pass_field.send_keys(self.password)
        self.safe_click(login_btn)

    def fill_text_box_form(self):
        try:
            elements_panel = self.wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "div.element-group")))
            self.safe_click(elements_panel)

            text_box_item = self.wait.until(EC.element_to_be_clickable((By.ID, "item-0")))
            self.safe_click(text_box_item)

            fullname_field = self.wait.until(EC.visibility_of_element_located((By.ID, "userName")))
            email_field = self.wait.until(EC.visibility_of_element_located((By.ID, "userEmail")))
            current_address_field = self.wait.until(EC.visibility_of_element_located((By.ID, "currentAddress")))
            permanent_address_field = self.wait.until(EC.visibility_of_element_located((By.ID, "permanentAddress")))
            submit_btn = self.wait.until(EC.element_to_be_clickable((By.ID, "submit")))
        except TimeoutException as exc:
            raise RuntimeError("Form elements not found (timeout)") from exc

        fullname_field.clear()
        fullname_field.send_keys("John Smith")
        email_field.clear()
        email_field.send_keys("john@gmail.com")
        current_address_field.clear()
        current_address_field.send_keys("Matatag Street Pinyahan Quezon City")
        permanent_address_field.clear()
        permanent_address_field.send_keys("Matatag Street Pinyahan Quezon City")

        self.safe_click(submit_btn)

    def download_file(self):
        try:
            elements_group = self.driver.find_elements(By.CSS_SELECTOR, "div.element-group")
            self.safe_click(elements_group[0])  # open the first group

            links = self.wait.until(EC.element_to_be_clickable((By.ID, "item-7")))
            self.safe_click(links)

            download_button = self.wait.until(EC.element_to_be_clickable((By.ID, "downloadButton")))
            self.safe_click(download_button)
        except TimeoutException as exc:
            raise RuntimeError("Download elements not found (timeout)") from exc

    def close(self):
        self.driver.quit()


# ==============================
# Main
# ==============================

if __name__ == "__main__":
    bot = DemoQABot(USERNAME, PASSWORD)
    try:
        bot.login()
        bot.fill_text_box_form()   # comment if not needed
        bot.download_file()        # comment if not needed
        input("Press Enter to close the browser...")
    finally:
        bot.close()
