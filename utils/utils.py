def quicksort(arr, key_func, low=0, high=None):
    if high is None:
        high = len(arr) - 1

    if low < high:
        pi = partition(arr, key_func, low, high)
        quicksort(arr, key_func, low, pi - 1)
        quicksort(arr, key_func, pi + 1, high)

    return arr


def partition(arr, key_func, low, high):
    pivot = arr[high]
    i = low - 1
    for j in range(low, high):
        if key_func(arr[j]) <= key_func(pivot):
            i += 1
            arr[i], arr[j] = arr[j], arr[i]
    arr[i + 1], arr[high] = arr[high], arr[i + 1]
    return i + 1
