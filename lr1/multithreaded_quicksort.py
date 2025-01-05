import threading

def quicksort(arr):
    if len(arr) <= 1:
        return arr
    pivot = arr[len(arr) // 2]
    left = [x for x in arr if x < pivot]
    middle = [x for x in arr if x == pivot]
    right = [x for x in arr if x > pivot]
    return quicksort(left) + middle + quicksort(right)

def threaded_quicksort(arr, results, index):
    results[index] = quicksort(arr)
    print(f"Thread sorted part: {results[index]}")

if __name__ == "__main__":
    array = [10, 7, 8, 1, 5, 2, 3, 9, 4, 6]
    threads = []
    results = [None] * 2

    mid = len(array) // 2
    left_part = array[:mid]
    right_part = array[mid:]

    threads.append(threading.Thread(target=threaded_quicksort, args=(left_part, results, 0)))
    threads.append(threading.Thread(target=threaded_quicksort, args=(right_part, results, 1)))

    for thread in threads:
        thread.start()

    for thread in threads:
        thread.join()

    sorted_array = quicksort(results[0] + results[1])
    print("Final sorted array:", sorted_array)