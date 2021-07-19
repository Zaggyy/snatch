import shutil

# Create a chunk of an array of specified size
def chunk(arr, size):
    return [arr[i:i + size] for i in range(0, len(arr), size)]

# Zip the directory and save it
def zip_directory(directory):
    shutil.make_archive(directory.replace('/', '_') + '.zip', 'zip', directory)
    