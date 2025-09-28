from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

# define driver, options and service
chrome_options = Options()
chrome_options.add_argument('--disable-search-engine-choice-screen')
service = Service('chromedriver-win64/chromedriver.exe')
driver = webdriver.Chrome(service=service, options=chrome_options)

# load the webpage
driver.get('https://demoqa.com/login')

# locate credentials and login button
username_field = WebDriverWait(driver, 10).until(
    EC.visibility_of_element_located((By.ID, 'userName')))
password_field = WebDriverWait(driver, 10).until(
    EC.visibility_of_element_located((By.ID, 'password')))

# login_button = WebDriverWait(driver, 10).until(
#     EC.visibility_of_element_located((By.ID, 'login')))

login_button = driver.find_element(By.ID, 'login')

# fill in username and password, and click the button
username_field.send_keys('malcolmulricson29')
password_field.send_keys('Passwrod29!')
# login_button.click()
driver.execute_script("arguments[0].click()", login_button)

input("Press enter to close the browser")
driver.quit()
