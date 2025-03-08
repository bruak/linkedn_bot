import time
import os
import sys
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from dotenv import load_dotenv  # Yeni: dotenv modülünü ekle

# .env dosyasını yükle
load_dotenv()

# Komut satırı argümanını kontrol et
headless_mode = False
if len(sys.argv) > 1:
    if sys.argv[1] == "1":
        headless_mode = True

# Chrome seçeneklerini tanımla
options = webdriver.ChromeOptions()
if headless_mode:
    options.add_argument("--headless")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--disable-gpu")
    options.add_argument("--window-size=1920,1080")
    print("Headless modda çalışıyor...")
else:
    options.add_argument("headless")
    print("Görünür modda çalışıyor...")

options.add_argument("--disable-gpu")
options.add_argument("--window-size=960,900")
options.add_argument("--disable-notifications")
options.add_argument("--disable-blink-features=AutomationControlled")

# Kullanacağınız driver'ı tanımlayın (Chrome örneği)
driver = webdriver.Chrome(options=options)

# page_number değerini kaydetmek için dosya yolu
page_number_file = "/app/data/page_number.txt"

# page_number değerini dosyaya yazan fonksiyon
def save_page_number(page_number):
    with open(page_number_file, "w") as f:
        f.write(str(page_number))

# page_number değerini dosyadan okuyan fonksiyon
def load_page_number():
    if os.path.exists(page_number_file):
        with open(page_number_file, "r") as f:
            return int(f.read())
    return 1

# 1. LinkedIn'e gidin ve giriş yapın
driver.get("https://www.linkedin.com/login")

username = WebDriverWait(driver, 15).until(
    EC.presence_of_element_located((By.ID, "username"))
)
password = driver.find_element(By.ID, "password")

# Buraya kendi giriş bilgilerinizi girin
username.send_keys(os.getenv("LINKEDIN_USERNAME"))
password.send_keys(os.getenv("LINKEDIN_PASSWORD"))
password.send_keys(Keys.RETURN)  # Enter'a basarak login ol

time.sleep(3)  # Girişin tam oturması için kısa bir bekleme

# 2. Arama sayfasına git (örneğin "42" anahtar kelimesiyle):
page_number = load_page_number()
search_url = (
    f"http://linkedin.com/search/results/people/?keywords=42&origin=CLUSTER_EXPANSION&page={page_number}&sid=RN9"
)
driver.get(search_url)
time.sleep(3)

# 3. Sayfalar arasında gezinme
retry_count = 0  # Yeni: Yeniden deneme sayacı
max_retries = 10  # Yeni: Maksimum yeniden deneme sayısı

while True:
    print(f"Sayfa {page_number} işleniyor...")
    
    # Sonsuz kaydırma
    scroll_count = 3
    for i in range(scroll_count):
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(2)

    # Bağlantı butonlarına tıklama
    try:
        connect_buttons = driver.find_elements(
            By.XPATH, "//button[contains(., 'Bağlantı kur') or contains(., 'Connect')]"
        )
        
        if not connect_buttons:
            print("Bağlantı kur/Connect butonu bulunamadı.")
        else:
            for btn in connect_buttons:
                try:
                    btn.click()  # Bağlantı kur butonuna bas
                    time.sleep(2)
                    
                    # "Not olmadan gönder" veya "Send now" butonuna tıkla
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
                    print(f"Bağlantı isteği gönderilirken hata: {e}")
                    try:
                        close_button = driver.find_element(By.XPATH, "//button[@aria-label='Dismiss']")
                        close_button.click()
                    except:
                        pass
                    continue

    except Exception as e:
        print(f"Bağlantı kur butonlarını işlerken hata oluştu: {e}")

    # Sonraki sayfaya geçiş yapma
    try:
        next_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable(
                (By.XPATH, "//button[contains(@aria-label, 'İleri') or contains(@aria-label, 'Next')]")
            )
        )
        next_button.click()
        page_number += 1
        save_page_number(page_number)  # page_number değerini kaydet
        time.sleep(5)  # Yeni sayfa yüklenmesi için bekleyin
        retry_count = 0  # Başarılı olduğunda retry sayacını sıfırla
    except Exception as e:
        retry_count += 1  # Yeni: Yeniden deneme sayacını artır
        print(f"Sonraki sayfa bulunamadı. Deneme {retry_count}/{max_retries}")
        
        if retry_count >= max_retries:
            print(f"{max_retries} deneme sonrası sonraki sayfa bulunamadı. İşlem sonlandırılıyor.")
            break
        else:
            # Sayfayı yenile ve tekrar dene
            driver.refresh()
            time.sleep(5)  # Sayfanın yenilenmesini bekle

# Tarayıcıyı kapat
time.sleep(2)
driver.quit()
print("İşlem tamamlandı.")