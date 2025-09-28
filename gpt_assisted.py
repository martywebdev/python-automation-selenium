import os
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from dotenv import load_dotenv

# Load credentials from .env
load_dotenv()
USERNAME = os.getenv("APP_USERNAME")
PASSWORD = os.getenv("APP_PASSWORD")

def create_driver():
    options = Options()
    options.add_argument("--disable-search-engine-choice-screen")
    # service = Service(ChromeDriverManager().install())
    service = Service('chromedriver-win64/chromedriver.exe')
    return webdriver.Chrome(service=service, options=options)

def login(driver, username, password):
    driver.get("https://demoqa.com/login")
    wait = WebDriverWait(driver, 10)

    user_field = wait.until(EC.visibility_of_element_located((By.ID, "userName")))
    pass_field = wait.until(EC.visibility_of_element_located((By.ID, "password")))
    login_btn = wait.until(EC.element_to_be_clickable((By.ID, "login")))

    user_field.send_keys(username)
    pass_field.send_keys(password)
    driver.execute_script("arguments[0].scrollIntoView(true);", login_btn)
    login_btn.click()

if __name__ == "__main__":
    driver = create_driver()
    try:
        login(driver, USERNAME, PASSWORD)
        input("Press enter to close the browser")
    finally:
        driver.quit()
