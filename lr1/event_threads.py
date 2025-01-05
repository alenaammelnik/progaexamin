import threading
import time

# Создание объекта Event
event = threading.Event()

# Поток 1: Устанавливает состояние события каждую секунду
def set_event():
    time.sleep(3)  # Ждём 3 секунды перед установкой события
    while True:
        event.set()
        print("Event set!")
        break

# Поток 2: Ждёт наступления события и выводит сообщение
def wait_for_event():
    event.wait()
    print("Event occurred")

# Поток 3: Выводит сообщение до наступления события и останавливается
def event_not_occurred():
    while not event.is_set():
        print("Event did not occur")
        time.sleep(1)

# Создание и запуск потоков
thread1 = threading.Thread(target=set_event)
thread2 = threading.Thread(target=wait_for_event)
thread3 = threading.Thread(target=event_not_occurred)

thread1.start()
thread2.start()
thread3.start()

# Ожидание завершения всех потоков
thread1.join()
thread2.join()
thread3.join()

print("Program completed.")