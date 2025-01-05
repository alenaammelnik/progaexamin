import concurrent.futures
import threading
import os
import time

# Файл для работы
FILE_NAME = "data.txt"

# Функция для записи данных в файл
def write_data():
    with open(FILE_NAME, 'w') as file:
        for i in range(1, 6):
            data = f"Line {i}\n"
            file.write(data)
            print(f"Written: {data.strip()}")
            time.sleep(0.5)  # Имитация задержки записи

# Функция для чтения данных из файла
def read_data():
    while not os.path.exists(FILE_NAME):
        time.sleep(0.1)  # Ожидание появления файла

    with open(FILE_NAME, 'r') as file:
        for line in file:
            print(f"Read: {line.strip()}")
            time.sleep(0.5)  # Имитация задержки чтения

# Создание потоков с синхронизацией через Future
with concurrent.futures.ThreadPoolExecutor() as executor:
    writer = executor.submit(write_data)
    reader = executor.submit(read_data)

    concurrent.futures.wait([writer, reader])

print("File operations completed.")