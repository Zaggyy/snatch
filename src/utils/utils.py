# Create a chunk of an array of specified size
def chunk(arr, size):
    return [arr[i:i + size] for i in range(0, len(arr), size)]