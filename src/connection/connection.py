import ftplib
import os

# Create a FTP connection to a server.
def connect_to_ftp_server(server_name, server_port, user, password):
    """
    (str, int) -> ftplib.FTP
    Connect to a FTP server.
    """
    ftp = ftplib.FTP()
    ftp.connect(server_name, server_port)
    ftp.login(user=user, passwd=password)
    return ftp

# List a directory on a FTP server.
def list_directory(ftp, directory):
    """
    (ftplib.FTP, str) -> list of str
    List a directory on a FTP server.
    """
    ftp.cwd(directory)
    return ftp.nlst()

# Download the files from the FTP server.
def download_files(ftp, directory, files, destination):
    """
    (ftplib.FTP, str, list of str, str) -> NoneType
    Download the files from the FTP server.
    """
    ftp.cwd(directory)
    for file in files:
        print("Downloading " + file + "...")
        path = os.path.join(destination, file)
        ftp.retrbinary("RETR " + file, open(path, 'wb').write)
        print("Downloaded " + file + ".")
