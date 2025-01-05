import threading

def thread_function():
    print(f"Thread name: {threading.current_thread().name}")

if __name__ == "__main__":
    threads = []
    for i in range(5):
        thread = threading.Thread(target=thread_function, name=f"Thread-{i+1}")
        threads.append(thread)
        thread.start()
    
    for thread in threads:
        thread.join()