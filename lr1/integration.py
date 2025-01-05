import math
import timeit
from threading import Thread, Lock

# Последовательное интегрирование
def integrate(f, a, b, *, n_iter=1000):
    step = (b - a) / n_iter
    result = 0
    for i in range(n_iter):
        x = a + i * step
        result += f(x) * step
    return result

# Многопоточное интегрирование с использованием Thread и Lock
def integrate_multithread(f, a, b, *, n_iter=1000, n_threads=4):
    step = (b - a) / n_iter
    results = [0] * n_threads
    lock = Lock()

    def worker(thread_idx, start, end):
        partial_result = 0
        for i in range(start, end):
            x = a + i * step
            partial_result += f(x) * step
        with lock:
            results[thread_idx] = partial_result

    threads = []
    chunk_size = n_iter // n_threads

    for i in range(n_threads):
        start = i * chunk_size
        end = start + chunk_size if i != n_threads - 1 else n_iter
        thread = Thread(target=worker, args=(i, start, end))
        threads.append(thread)
        thread.start()

    for thread in threads:
        thread.join()

    return sum(results)

# Тестирование и оценка времени выполнения
if __name__ == "__main__":
    import timeit

    f = math.sin
    a, b = 0, math.pi / 2

    # Последовательное интегрирование
    seq_time_10_4 = timeit.timeit(lambda: integrate(f, a, b, n_iter=10**4), number=1)
    seq_time_10_5 = timeit.timeit(lambda: integrate(f, a, b, n_iter=10**5), number=1)
    seq_time_10_6 = timeit.timeit(lambda: integrate(f, a, b, n_iter=10**6), number=1)

    # Многопоточное интегрирование
    mt_time_10_4 = timeit.timeit(lambda: integrate_multithread(f, a, b, n_iter=10**4, n_threads=4), number=1)
    mt_time_10_5 = timeit.timeit(lambda: integrate_multithread(f, a, b, n_iter=10**5, n_threads=4), number=1)
    mt_time_10_6 = timeit.timeit(lambda: integrate_multithread(f, a, b, n_iter=10**6, n_threads=4), number=1)

    # Вывод результатов
    print(f"Последовательное время для 10^4 итераций: {seq_time_10_4:.5f} секунд")
    print(f"Последовательное время для 10^5 итераций: {seq_time_10_5:.5f} секунд")
    print(f"Последовательное время для 10^6 итераций: {seq_time_10_6:.5f} секунд")

    print(f"Многопоточное время для 10^4 итераций: {mt_time_10_4:.5f} секунд")
    print(f"Многопоточное время для 10^5 итераций: {mt_time_10_5:.5f} секунд")
    print(f"Многопоточное время для 10^6 итераций: {mt_time_10_6:.5f} секунд")
