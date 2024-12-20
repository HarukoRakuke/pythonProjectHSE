import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from webdriver_manager.chrome import ChromeDriverManager
from datetime import datetime
import re

# Инициализация драйвера

def initialize_webdriver(block_images=True):
    chrome_options = webdriver.ChromeOptions()
    if block_images:
        preferences = {"profile.managed_default_content_settings.images": 2}
        chrome_options.add_experimental_option("prefs", preferences)
    driver_service = Service(ChromeDriverManager().install())
    return webdriver.Chrome(service=driver_service, options=chrome_options)

# Форматирование URL для песни

def construct_song_url(song_name):
    base = "https://genius.com/"
    processed_name = re.sub(r"[^\w\s]", "", song_name).strip()
    processed_name = re.sub(r"\s+", "-", processed_name)
    return f"{base}mrkitty-{processed_name}-lyrics"

# Безопасная загрузка страницы

def load_page_safely(driver, url, timeout=20):
    try:
        driver.set_page_load_timeout(timeout)
        driver.get(url)
    except TimeoutException:
        print(f"Ошибка загрузки страницы: {url}")
        driver.execute_script("window.stop();")

# Основная логика

browser = initialize_webdriver()
waiter = WebDriverWait(browser, 20)

song_list_url = 'https://genius.com/artists/Mrkitty/songs'
browser.get(song_list_url)

# Сбор названий песен

try:
    song_elements = waiter.until(EC.presence_of_all_elements_located(
        (By.XPATH, '//*[@id="application"]/main/div[1]/div/div[3]/div[3]/div/div[2]/ul/li/a/div[2]/h3')
    ))
    all_song_titles = [el.text for el in song_elements]
except Exception as err:
    print("Ошибка при загрузке песен:", err)
    all_song_titles = []

collected_data = []

for song_title in all_song_titles:
    song_link = construct_song_url(song_title)
    print(f"Собираем данные для: {song_title}")
    load_page_safely(browser, song_link)

    details = {
        "Название": song_title,
        "Дата выхода": "Не указано",
        "Текст": "Не указано",
    }

    try:
        date_text = waiter.until(
            lambda d: d.find_element(By.XPATH,
                '//*[@id="application"]/main/div[1]/div[3]/div[1]/div[2]/div/span[1]/span | '
                '//*[@id="application"]/main/div[1]/div[3]/div[1]/div[2]/div[2]/span[1]/span')
        ).text
        details["Дата выхода"] = datetime.strptime(date_text, "%b. %d, %Y")
    except:
        print(f"Не получилось получить дату выхода для: {song_title}")

    try:
        lyrics_content = waiter.until(EC.presence_of_element_located(
            (By.XPATH, '//*[@id="lyrics-root"]/div[2]')
        )).text
        details["Текст"] = lyrics_content
    except:
        print(f"Текст не загружен для: {song_title}")

    collected_data.append(details)

# Создание DataFrame и сохранение результата

dataframe = pd.DataFrame(collected_data, columns=["Название", "Дата выхода", "Текст"])
dataframe["Дата выхода"] = pd.to_datetime(dataframe["Дата выхода"], errors='coerce')
dataframe = dataframe.sort_values(by="Дата выхода")

dataframe.to_excel('mrkitty_song_data.xlsx', index=False, engine='openpyxl')

browser.quit()
print("Готово! Данные сохранены.")
