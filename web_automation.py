from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
import time

# Updated path to ChromeDriver
driver_path = r'C:\Users\jaden\OneDrive\Documents\chromedriver-win64\chromedriver.exe'
service = Service(driver_path)

# Set up Chrome options for headless mode
chrome_options = Options()
chrome_options.add_argument("--headless")  # Enables headless mode
chrome_options.add_argument("--disable-gpu")  # Disable GPU rendering (optional but recommended for headless)
chrome_options.add_argument("--window-size=1920,1080")  # Set the window size if required

# Initialize the driver with headless options
driver = webdriver.Chrome(service=service, options=chrome_options)
driver.get('https://www.screener.in/')
wait = WebDriverWait(driver, 15)

try:
    print("Finding and clicking the login button...")
    login_button = wait.until(EC.element_to_be_clickable((By.XPATH, '/html/body/nav/div[2]/div/div/div/div[2]/div[2]/a[1]')))
    login_button.click()

    print("Waiting for login fields to be present...")
    email_field = wait.until(EC.presence_of_element_located((By.XPATH, '/html/body/main/div[2]/div[2]/form/div[1]/input')))
    password_field = driver.find_element(By.XPATH, '/html/body/main/div[2]/div[2]/form/div[2]/input')

    print("Entering email and password...")
    email_field.send_keys('koget44912@janfab.com')  # Replace with your email
    password_field.send_keys('automation')  # Replace with your password

    submit_button = driver.find_element(By.XPATH, '/html/body/main/div[2]/div[2]/form/button')  # Replace with the actual submit button XPath
    print("Clicking submit button...")
    submit_button.click()

    print("Waiting for the main page to load after login...")
    wait.until(EC.presence_of_element_located((By.XPATH, '/html/body/nav/div[2]/div/div/div/div[2]/div[1]/div/input')))

    print("Finding and performing the search...")
    search_box = driver.find_element(By.XPATH, '/html/body/nav/div[2]/div/div/div/div[2]/div[1]/div/input')
    search_box.send_keys('tcs')  # Replace with your search query
    search_box.send_keys(Keys.RETURN)

    print("Waiting for Export to Excel button...")
    export_button = wait.until(EC.element_to_be_clickable((By.XPATH, '/html/body/main/div[3]/div[1]/form/button')))
    print("Clicking Export to Excel button...")
    export_button.click()
    time.sleep(5)

finally:
    driver.quit()
