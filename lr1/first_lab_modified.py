import math
import concurrent.futures as ftres
from functools import partial
from timeit import timeit

# Численное интегрирование с последовательным подходом
def integrate(f, a, b, *, n_iter=1000):
    step = (b - a) / n_iter
    total = 0
    for i in range(n_iter):
        x = a + i * step
        total += f(x) * step
    return total

# Численное интегрирование с использованием многопоточности или многопроцессности
def integrate_async(f, a, b, *, n_jobs=2, n_iter=1000, executor_class=ftres.ThreadPoolExecutor):
    step = (b - a) / n_jobs
    executor = executor_class(max_workers=n_jobs)
    spawn = partial(executor.submit, integrate, f, n_iter=n_iter // n_jobs)
    intervals = [(a + i * step, a + (i + 1) * step) for i in range(n_jobs)]
    futures = [spawn(start, end) for start, end in intervals]
    return sum(f.result() for f in ftres.as_completed(futures))

# Замер времени работы для заданных параметров
def benchmark():
    # Параметры задачи
    n_iter = 10**6
    a, b = 0, math.pi / 2
    func = math.atan

    # Параметры многопоточной/многопроцессной интеграции
    thread_times = []
    process_times = []

    for n_jobs in [2, 4, 6]:
        # Многопоточность
        thread_time = timeit(
            lambda: integrate_async(func, a, b, n_jobs=n_jobs, n_iter=n_iter, executor_class=ftres.ThreadPoolExecutor),
            number=100
        )
        thread_times.append((n_jobs, thread_time))

        # Многопроцессность
        process_time = timeit(
            lambda: integrate_async(func, a, b, n_jobs=n_jobs, n_iter=n_iter, executor_class=ftres.ProcessPoolExecutor),
            number=100
        )
        process_times.append((n_jobs, process_time))

    # Вывод результатов
    print("Многопоточность (ThreadPoolExecutor):")
    for n_jobs, time in thread_times:
        print(f"Число потоков: {n_jobs}, время: {time:.3f} мс")

    print("\nМногопроцессность (ProcessPoolExecutor):")
    for n_jobs, time in process_times:
        print(f"Число процессов: {n_jobs}, время: {time:.3f} мс")

if __name__ == "__main__":
    # Последовательное вычисление интеграла
    result_seq = integrate(math.atan, 0, math.pi / 2, n_iter=10**6)
    print(f"Последовательный результат: {result_seq:.6f}")

    # Многопоточное вычисление интеграла
    result_thread = integrate_async(
        math.atan, 0, math.pi / 2, n_jobs=4, n_iter=10**6, executor_class=ftres.ThreadPoolExecutor
    )
    print(f"Многопоточный результат: {result_thread:.6f}")

    # Многопроцессное вычисление интеграла
    result_process = integrate_async(
        math.atan, 0, math.pi / 2, n_jobs=4, n_iter=10**6, executor_class=ftres.ProcessPoolExecutor
    )
    print(f"Многопроцессный результат: {result_process:.6f}")

    # Замер времени
    benchmark()