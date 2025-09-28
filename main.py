import os
from dotenv import load_dotenv
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

# Load credentials from .env
load_dotenv()
USERNAME = os.getenv("APP_USERNAME")
PASSWORD = os.getenv("APP_PASSWORD")


def create_driver():
    '''define driver, options and service'''
    chrome_options = Options()
    chrome_options.add_argument('--disable-search-engine-choice-screen')
    service = Service('chromedriver-win64/chromedriver.exe')
    return webdriver.Chrome(service=service, options=chrome_options)


def login(driver):

    # load the webpage
    driver.get('https://demoqa.com/login')
    wait = WebDriverWait(driver, 10)

    # locate credentials and login button
    username_field = wait.until(
        EC.visibility_of_element_located((By.ID, 'userName')))
    password_field = wait.until(
        EC.visibility_of_element_located((By.ID, 'password')))

    # login_button = WebDriverWait(driver, 10).until(
    #     EC.visibility_of_element_located((By.ID, 'login')))

    login_button = driver.find_element(By.ID, 'login')

    # fill in username and password, and click the button
    username_field.send_keys('malcolmulricson29')
    password_field.send_keys('Passwrod29!')
    # login_button.click()
    driver.execute_script("arguments[0].click()", login_button)


def fill_text_box_form(driver):
    # locate the elements dropdown
    wait = WebDriverWait(driver, 10)
    elements =wait.until(
        EC.visibility_of_element_located((
            By.XPATH,'//*[@id="app"]/div/div/div/div[1]/div/div/div[1]/span/div')))

    elements.click()

    text_box =wait.until(
        EC.visibility_of_element_located((By.ID, 'item-0')))

    text_box.click()
    # locate the form fields
    fullname_field =wait.until(EC.visibility_of_element_located((By.ID, 'userName')))
    email_field =wait.until(EC.visibility_of_element_located((By.ID, 'userEmail')))
    current_address_field =wait.until(EC.visibility_of_element_located((By.ID, 'currentAddress')))
    permanent_address_field =wait.until(EC.visibility_of_element_located((By.ID, 'permanentAddress')))
    submit_button = driver.find_element(By.ID, 'submit')
    # fill in the form fields
    fullname_field.send_keys('John Smith')
    email_field.send_keys('john@gmail.com')
    current_address_field.send_keys('Matatag Street Pinyahan Quezon city')
    permanent_address_field.send_keys('Matatag Street Pinyahan Quezon city')
    driver.execute_script("arguments[0].click()", submit_button)

if __name__ == '__main__':
    driver = create_driver()

    try:
        login(driver)
        fill_text_box_form(driver=driver)
        input("Press enter to close the browser")
    finally:

        driver.quit()
