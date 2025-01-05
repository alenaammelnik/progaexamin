import threading
from math import factorial

def calculate_factorial(number, results, index):
    results[index] = factorial(number)
    print(f"Factorial of {number} is {results[index]}")

if __name__ == "__main__":
    numbers = [5, 7, 10]
    results = [None] * len(numbers)

    threads = []
    for i, number in enumerate(numbers):
        thread = threading.Thread(target=calculate_factorial, args=(number, results, i))
        threads.append(thread)
        thread.start()

    for thread in threads:
        thread.join()

    print("Results:", results)