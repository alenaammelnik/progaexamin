import concurrent.futures
import threading
import urllib.request
import os

# Папка для сохранения изображений
SAVE_DIR = "images"
os.makedirs(SAVE_DIR, exist_ok=True)

# Список URL изображений
image_urls = [
    "https://via.placeholder.com/600/92c952",
    "https://via.placeholder.com/600/771796",
    "https://via.placeholder.com/600/24f355",
    "https://via.placeholder.com/600/d32776",
    "https://via.placeholder.com/600/f66b97"
]

# Ограничение количества одновременных загрузок
MAX_WORKERS = 3
semaphore = threading.Semaphore(MAX_WORKERS)

def download_image(url):
    with semaphore:
        try:
            image_name = os.path.basename(url)
            image_path = os.path.join(SAVE_DIR, image_name)
            
            urllib.request.urlretrieve(url, image_path)
            print(f"Downloaded: {image_name}")
        except Exception as e:
            print(f"Failed to download {url}: {e}")

# Асинхронная загрузка изображений
with concurrent.futures.ThreadPoolExecutor() as executor:
    futures = [executor.submit(download_image, url) for url in image_urls]
    
    for future in concurrent.futures.as_completed(futures):
        future.result()

print("All downloads completed.")