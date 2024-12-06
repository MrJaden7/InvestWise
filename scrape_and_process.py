import os
import time
import pandas as pd
from fpdf import FPDF
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options

# Web scraping section
driver_path = r'C:\Users\jaden\OneDrive\Documents\chromedriver-win64\chromedriver.exe'
download_path = r'C:\Users\jaden\OneDrive\Desktop\major project'
service = Service(driver_path)
chrome_options = Options()
chrome_options.add_argument("--headless")  
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-gpu")
chrome_options.add_argument(f'--window-size=1920,1080')
chrome_options.add_experimental_option("prefs", {
    "download.default_directory": download_path,  # Set default download location
    "download.prompt_for_download": False,  
    "download.directory_upgrade": True,
    "safebrowsing.enabled": True,
})


driver = webdriver.Chrome(service=service, options=chrome_options)
wait = WebDriverWait(driver, 15)
driver.get('https://www.screener.in/')

try:
    login_button = wait.until(EC.element_to_be_clickable((By.XPATH, '/html/body/nav/div[2]/div/div/div/div[2]/div[2]/a[1]')))
    login_button.click()
    
    email_field = wait.until(EC.presence_of_element_located((By.XPATH, '/html/body/main/div[2]/div[2]/form/div[1]/input')))
    password_field = driver.find_element(By.XPATH, '/html/body/main/div[2]/div[2]/form/div[2]/input')
    email_field.send_keys('your_email@example.com')
    password_field.send_keys('your_password')
    
    submit_button = driver.find_element(By.XPATH, '/html/body/main/div[2]/div[2]/form/button')
    submit_button.click()
    
    search_box = wait.until(EC.presence_of_element_located((By.XPATH, '/html/body/nav/div[2]/div/div/div/div[2]/div[1]/div/input')))
    search_box.send_keys('tcs')  # Example company
    search_box.send_keys(Keys.RETURN)
    
    export_button = wait.until(EC.element_to_be_clickable((By.XPATH, '/html/body/main/div[3]/div[1]/form/button')))
    export_button.click()
    time.sleep(5)  
    
finally:
    driver.quit()

# Find the most recent file in the download directory
files = os.listdir(download_path)
files = [f for f in files if f.endswith('.xlsx')]
if not files:
    raise FileNotFoundError("No Excel file was downloaded.")


files.sort(key=lambda x: os.path.getmtime(os.path.join(download_path, x)), reverse=True)
input_file = os.path.join(download_path, files[0])
output_file = os.path.join(download_path, os.path.splitext(os.path.basename(input_file))[0] + "_cleaned.pdf")

# Initialize the PDF
pdf = FPDF()
pdf.set_auto_page_break(auto=True, margin=15)

# Load the Excel file and process it
excel_data = pd.ExcelFile(input_file)
sheet_names = excel_data.sheet_names

for sheet in sheet_names:
    df = excel_data.parse(sheet)
    df.dropna(how="all", inplace=True)  # Remove rows with all null values
    df.dropna(axis=1, how="all", inplace=True)  # Remove columns with all null values
    df.fillna("", inplace=True)  # Replace remaining NaNs with an empty string

    pdf.add_page()
    pdf.set_font("Helvetica", "B", 12)
    pdf.cell(200, 10, f"Sheet: {sheet}", ln=True, align="C")

    pdf.set_font("Helvetica", "", 10)
    data = [df.columns.tolist()] + df.values.tolist()
    
    for row in data:
        row_text = " | ".join(str(cell) for cell in row if cell)
        pdf.cell(200, 10, row_text.encode('latin-1', 'replace').decode('latin-1'), ln=True)

pdf.output(output_file)
print(f"PDF created successfully at {output_file}")
