import time
import os
import sys
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from dotenv import load_dotenv

load_dotenv()

headless_mode = False
if len(sys.argv) > 1:
    if sys.argv[1] == "1":
        headless_mode = True

options = webdriver.ChromeOptions()
if headless_mode:
    options.add_argument("--headless")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--disable-gpu")
    options.add_argument("--window-size=1920,1080")
    print("Running in headless mode...")
else:
    options.add_argument("headless")
    print("Running in visible mode...")

options.add_argument("--disable-gpu")
options.add_argument("--window-size=960,900")
options.add_argument("--disable-notifications")
options.add_argument("--disable-blink-features=AutomationControlled")

driver = webdriver.Chrome(options=options)

page_number_file = "/app/data/page_number.txt"

def save_page_number(page_number):
    with open(page_number_file, "w") as f:
        f.write(str(page_number))

def load_page_number():
    if os.path.exists(page_number_file):
        with open(page_number_file, "r") as f:
            return int(f.read())
    return 1

driver.get("https://www.linkedin.com/login")

username = WebDriverWait(driver, 15).until(
    EC.presence_of_element_located((By.ID, "username"))
)
password = driver.find_element(By.ID, "password")

username.send_keys(os.getenv("LINKEDIN_USERNAME"))
password.send_keys(os.getenv("LINKEDIN_PASSWORD"))
password.send_keys(Keys.RETURN)

time.sleep(3)

page_number = load_page_number()
search_url = (
    f"http://linkedin.com/search/results/people/?keywords=42&origin=CLUSTER_EXPANSION&page={page_number}&sid=RN9"
)
driver.get(search_url)
time.sleep(3)

retry_count = 0
max_retries = 10

while True:
    print(f"Processing page {page_number}...")
    
    scroll_count = 3
    for i in range(scroll_count):
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(2)

    try:
        connect_buttons = driver.find_elements(
            By.XPATH, "//button[contains(., 'Bağlantı kur') or contains(., 'Connect')]"
        )
        
        if not connect_buttons:
            print("Connect button not found.")
        else:
            for btn in connect_buttons:
                try:
                    btn.click()
                    time.sleep(2)
                    
                    send_now_button = WebDriverWait(driver, 5).until(
                        EC.element_to_be_clickable(
                            (
                                By.XPATH,
                                "//button[contains(., 'Not olmadan gönder') or contains(., 'Send now') or contains(., 'Gönder') or contains(., 'Send')]",
                            )
                        )
                    )
                    send_now_button.click()
                    time.sleep(2)
                    
                except Exception as e:
                    print(f"Error sending connection request: {e}")
                    try:
                        close_button = driver.find_element(By.XPATH, "//button[@aria-label='Dismiss']")
                        close_button.click()
                    except:
                        pass
                    continue

    except Exception as e:
        print(f"Error processing connect buttons: {e}")

    try:
        next_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable(
                (By.XPATH, "//button[contains(@aria-label, 'İleri') or contains(@aria-label, 'Next')]")
            )
        )
        next_button.click()
        page_number += 1
        save_page_number(page_number)
        time.sleep(5)
        retry_count = 0
    except Exception as e:
        retry_count += 1
        print(f"Next page not found. Attempt {retry_count}/{max_retries}")
        
        if retry_count >= max_retries:
            print(f"Next page not found after {max_retries} attempts. Terminating process.")
            break
        else:
            driver.refresh()
            time.sleep(5)

time.sleep(2)
driver.quit()
print("Process completed.")