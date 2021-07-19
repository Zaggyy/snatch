import shutil
import sys
import os
import threading

from config.config import read_yml_config
from connection.connection import connect_to_ftp_server, download_files, list_directory
from utils.utils import chunk, zip_directory

# Check the number of command line arguments
if len(sys.argv) != 2:
    print("Usage: python3 main.py <config file>")
    sys.exit(1)

# Read YAML config file
config = read_yml_config(sys.argv[1])['ftp']

if config is not None:
    print("Config file loaded successfully")
    host = config["host"]
    port = config["port"]
    username = config["user"]
    password = config["password"]
    try:
        # Try to connect to the server
        connection = connect_to_ftp_server(host, port, username, password)
        files = list_directory(connection, config['directory'])
        connection.abort()

        file_chunks = chunk(files, config['chunk_size'])
        print(f"{len(files)} files found")
        print(f"{len(file_chunks)} chunks created")

        # Generate a temporary directory name
        temp_dir = config['directory'] + '_temp'

        # Make sure that temp_dir exists
        os.makedirs(temp_dir, exist_ok=True)

        # Create a thread for each chunk
        for index, chunk in enumerate(file_chunks):
            print(f"Starting thread {index + 1}")
            # Create a FTP connection
            connection = connect_to_ftp_server(host, port, username, password)
            # Download the chunk via thread
            threading.Thread(target=lambda: download_files(connection, config['directory'], chunk, temp_dir)).start()

        # Wait for all threads to finish
        for thread in threading.enumerate():
            if thread is not threading.currentThread():
                thread.join()

        # Zip the downloaded files
        print("Zipping files")
        zip_directory(temp_dir)
        print(f"Zipping completed")

        # Remove the temporary directory even if it's not empty
        print("Removing temporary directory")
        shutil.rmtree(temp_dir)
        print("Temporary directory removed")

        print("All done")
    except ConnectionRefusedError:
        print("Failed to connect to the server")