import threading
import time

class Queue:
    def __init__(self):
        self.queue = []
        self.lock = threading.RLock()

    def enqueue(self, item):
        with self.lock:
            self.queue.append(item)
            print(f"Enqueued: {item}")

    def dequeue(self):
        with self.lock:
            if len(self.queue) == 0:
                print("Queue is empty!")
                return None
            item = self.queue.pop(0)
            print(f"Dequeued: {item}")
            return item

# Создание барьера для синхронизации
barrier = threading.Barrier(2)

# Серверная логика
def server():
    print("Server is initializing...")
    time.sleep(2)
    print("Server is ready.")
    barrier.wait()
    print("Server received request and processed it.")

# Клиентская логика
def client():
    print("Client is waiting for server...")
    barrier.wait()
    print("Client sent request.")

# Создание и запуск потоков
server_thread = threading.Thread(target=server)
client_thread = threading.Thread(target=client)

server_thread.start()
client_thread.start()

server_thread.join()
client_thread.join()

print("Server-client communication completed.")