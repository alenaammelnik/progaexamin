import threading
from urllib.request import urlopen, Request
from urllib.error import URLError, HTTPError

def make_request(url):
    try:
        req = Request(url, headers={'User-Agent': 'Mozilla/5.0'})  # Добавляем заголовок User-Agent
        with urlopen(req) as response:
            print(f"Response from {url}: {response.status}, {response.reason}")
    except HTTPError as e:
        print(f"HTTP error: {e.code} for {url}")
    except URLError as e:
        print(f"URL error: {e.reason} for {url}")
    except Exception as e:
        print(f"Unexpected error for {url}: {e}")

if __name__ == "__main__":
    # Реальные URL
    urls = [
        "https://jsonplaceholder.typicode.com/posts/1",   # API-запрос
        "https://httpbin.org/get",                        # Тестовый сервис
        "https://jsonplaceholder.typicode.com/comments",  # API-запрос с большим количеством данных
    ]

    threads = []
    for url in urls:
        thread = threading.Thread(target=make_request, args=(url,))
        threads.append(thread)
        thread.start()

    for thread in threads:
        thread.join()

    print("All requests completed.")