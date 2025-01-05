import threading
from urllib.request import urlopen, urlretrieve
from urllib.error import URLError, HTTPError

def download_file(url, filename):
    try:
        # Открываем URL и сохраняем файл
        urlretrieve(url, filename)
        print(f"Downloaded {filename}")
    except HTTPError as e:
        print(f"HTTP error: {e.code} for {url}")
    except URLError as e:
        print(f"Failed to reach server: {e.reason} for {url}")
    except Exception as e:
        print(f"Unexpected error: {e} for {url}")

if __name__ == "__main__":
    # Реальные URL (пример для загрузки картинок)
    urls = [
        ("https://via.placeholder.com/150", "image1.jpg"),
        ("https://via.placeholder.com/300", "image2.jpg"),
        ("https://via.placeholder.com/450", "image3.jpg"),
    ]

    threads = []
    for url, filename in urls:
        thread = threading.Thread(target=download_file, args=(url, filename))
        threads.append(thread)
        thread.start()

    for thread in threads:
        thread.join()

    print("All downloads completed.")