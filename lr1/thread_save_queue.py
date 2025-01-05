import threading

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

# Пример работы с очередью в многопоточности
def producer(queue, items):
    for item in items:
        queue.enqueue(item)


def consumer(queue, count):
    for _ in range(count):
        queue.dequeue()

queue = Queue()

# Создание потоков для добавления и удаления элементов
producer_thread = threading.Thread(target=producer, args=(queue, [1, 2, 3, 4, 5]))
consumer_thread = threading.Thread(target=consumer, args=(queue, 5))

producer_thread.start()
consumer_thread.start()

producer_thread.join()
consumer_thread.join()

print("Queue operations completed.")