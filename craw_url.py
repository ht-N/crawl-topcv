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
options.add_argument(f'--user-data-dir={profile_path}')
options.add_argument(f'--profile-directory={name}')
# options.add_argument("headless")

driver = webdriver.Chrome(service = service, options=options)

url_sp = []

for i in range(1, 126):
    url = f"https://www.topcv.vn/tim-viec-lam-cong-nghe-thong-tin-cr257?type_keyword=0&page={i}&category_family=r257"
    print(f"Try getting url number: {i}")

    driver.get(url)

    # Check if captcha appears and wait for manual solving if needed
    try:
        # Wait up to 60 seconds for job listings to appear
        print("Waiting for page to load or captcha to be solved...")
        WebDriverWait(driver, 60).until(
            EC.presence_of_all_elements_located((By.XPATH, "//h3[@class='title ']//a"))
        )
        print("Page loaded successfully!")
    except:
        # If timeout occurs, ask for manual intervention
        print("Captcha might be present. Please solve it manually.")
        input("Press Enter after solving the captcha...")
        # Wait a bit more after manual intervention
        time.sleep(3)

    elements = driver.find_elements(By.XPATH, "//h3[@class='title ']//a")

    for element in elements:
        # Lấy giá trị của thuộc tính href
        href_value = element.get_attribute("href")
        url_sp.append(href_value)

    print(f"Total URLs collected so far: {len(url_sp)}")

driver.quit()

df = pd.DataFrame(url_sp, columns=["URL"])

# Lưu DataFrame thành tệp CSV
df.to_csv("urls.csv", index=False)