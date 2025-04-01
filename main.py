from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd
import time

name = "Profile 6"
profile_path = fr"C:/Users/hello/AppData/Local/Google/Chrome/User Data"

webdriver_path = fr"chromedriver-win64\chromedriver.exe"
service = Service(webdriver_path)
options = webdriver.ChromeOptions()

options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")
options.add_argument(f'--user-data-dir={profile_path}')
options.add_argument(f'--profile-directory={name}')
# options.add_argument("headless")

driver = webdriver.Chrome(service=service, options=options)
df = pd.read_csv('data/urls_topcv.csv')
df = df.iloc[:1000]
# Truy cập cột 'URL' trong DataFrame
urls = df['URL'].tolist()

job_data = []
processed = 0
total = len(urls)

for url in urls:
    processed += 1
    print(f"Processing {processed}/{total}: {url}")
    
    try:
        driver.get(url)
        
        # Check if captcha appears and wait for manual solving if needed
        try:
            # Wait up to 30 seconds for job details to appear
            print("Waiting for page to load or captcha to be solved...")
            WebDriverWait(driver, 30).until(
                EC.presence_of_element_located((By.XPATH, "//div[contains(@class, 'company-field')]"))
            )
        except:
            # If timeout occurs, ask for manual intervention
            time.sleep(3)
        
        # Extract job information
        job_info = {}
        
        # Get Field
        try:
            field_element = driver.find_element(By.XPATH, "//div[contains(@class, 'company-field')]/div[contains(@class, 'company-value')]")
            job_info['Field'] = field_element.text.strip()
        except:
            job_info['Field'] = "N/A"
            
        # Get Experience
        try:
            exp_element = driver.find_element(By.XPATH, "//div[@id='job-detail-info-experience']//div[contains(@class, 'job-detail__info--section-content-value')]")
            job_info['Experience'] = exp_element.text.strip()
        except:
            job_info['Experience'] = "N/A"
            
        # Get Location
        try:
            location_element = driver.find_element(By.XPATH, "(//div[contains(@class, 'job-detail__info--section')]/div[contains(@class, 'job-detail__info--section-content-value')])[2]")
            job_info['Location'] = location_element.text.strip()
        except:
            job_info['Location'] = "N/A"
            
        # Get Company Size
        try:
            size_element = driver.find_element(By.XPATH, "//div[contains(@class, 'company-scale')]/div[contains(@class, 'company-value')]")
            job_info['Company Size'] = size_element.text.strip()
        except:
            job_info['Company Size'] = "N/A"
            
        # Get Salary
        try:
            salary_element = driver.find_element(By.XPATH, "//div[contains(@class, 'job-detail__info--section-content')]/div[contains(@class, 'job-detail__info--section-content-value')]")
            job_info['Salary'] = salary_element.text.strip()
        except:
            job_info['Salary'] = "N/A"
        
        # Add job URL for reference
        job_info['URL'] = url
        
        job_data.append(job_info)
        print(f"Successfully extracted data from job {processed}")
        
        # Add a small delay between requests to avoid being blocked
        time.sleep(2)
        
    except Exception as e:
        print(f"Error processing URL {url}: {str(e)}")
        continue

driver.quit()

# Create DataFrame from the collected data
jobs_df = pd.DataFrame(job_data)

# Save to CSV
jobs_df.to_csv('data/job_details2.csv', index=False)
print(f"Job details saved, len of jobs: {len(job_data)}")