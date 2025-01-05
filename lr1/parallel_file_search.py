import os
import threading
import fnmatch
import time

# Флаг для остановки потоков после нахождения файла
found_event = threading.Event()

# Функция поиска файла
def search_files(directory, pattern):
    for root, dirs, files in os.walk(directory):
        if found_event.is_set():
            return
        for file in files:
            if fnmatch.fnmatch(file, pattern):
                print(f"File found: {os.path.join(root, file)}")
                found_event.set()
                return
            time.sleep(0.1)  # Имитация задержки обработки

# Основная логика программы
def main():
    directory = input("Enter directory to search: ")
    pattern = input("Enter filename pattern (e.g., *.txt): ")

    # Получаем список поддиректорий для обработки разными потоками
    subdirs = [os.path.join(directory, d) for d in os.listdir(directory) if os.path.isdir(os.path.join(directory, d))]

    threads = []
    for subdir in subdirs:
        thread = threading.Thread(target=search_files, args=(subdir, pattern))
        threads.append(thread)
        thread.start()

    # Ожидаем завершения всех потоков
    for thread in threads:
        thread.join()

    if not found_event.is_set():
        print("File not found.")

if __name__ == "__main__":
    main()