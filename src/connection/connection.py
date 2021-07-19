import ftputil
import os

# Create a FTP connection to a server.
def connect_to_ftp_server(server_name, user, password):
    ftp = ftputil.FTPHost(server_name, user, password)
    return ftp

# Traverse all directories recursively on the FTP server.
def traverse(ftp, directory, depth=0):
    files = ftp.listdir(directory)
    return_files = []
    for file in files:
        file_path = os.path.join(directory, file)
        # Check if a file is a directory.
        if ftp.path.isdir(file_path):
            print("Traversing directory: " + file + "...")
            # Merge with the return_files
            return_files.extend(traverse(ftp, file_path, depth+1))
        else:
            print("Found file: " + file)
            return_files.append(file_path)

    return return_files
    

# Download the files from the FTP server.
def download_files(ftp, files, destination):
    ftp.chdir('/')
    for file in files:
        print("Downloading " + file + "...")
        path = os.path.join(destination, file)
        # Make sure the path exists.
        if not os.path.exists(os.path.dirname(path)):
            os.makedirs(os.path.dirname(path))
        
        ftp.download(file, path)
        print("Downloaded " + file + ".")
