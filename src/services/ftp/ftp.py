from services.log.Logger import Logger
import ftputil
import os


class Connection:

    connected = False

    def __init__(self, config, connect=True, num=0):
        self.logger = Logger('ftp' if num < 1 else 'ftp-{}'.format(num))
        self.config = config
        if connect:
            self.connect()

    def connect(self):
        if self.connected is True:
            return
        try:
            self.ftp = ftputil.FTPHost(
                self.config['host'], self.config['user'], self.config['password'])
            self.logger.success('Connection established.')
        except ftputil.error.FTPError as e:
            self.logger.error('Connection failed: ' + str(e))
            raise e

    # Traverse the FTP directory and return the file list
    def traverse(self, directory):
        if self.connected is False:
            self.connect()
        self.logger.info('Traversing directory: ' + directory)
        files = self.ftp.listdir(directory)
        return_files_dict = {}

        for file in files:
            file_path = os.path.join(directory, file)
            # Check if a file is a directory
            if self.ftp.path.isdir(file_path):
                self.logger.info('Found directory: ' + file_path)
                return_files_dict.update(self.traverse(file_path))
            else:
                self.logger.info('Found file: ' + file_path)
                return_files_dict[file_path] = self.ftp.path.getsize(file_path)

        return return_files_dict

    def download(self, files, destination):
        if self.connected is False:
            self.connect()
        for file in files:
            self.logger.info('Downloading file: ' + file)
            path = os.path.join(destination, file)

            try:
                # Make sure that the path exists
                if not os.path.exists(os.path.dirname(path)):
                    os.makedirs(os.path.dirname(path))

                self.ftp.download(file, path)
                self.logger.success('Downloaded file: ' + file)
            except:
                self.logger.error('File download failed: ' + file)
        self.disconnect()

    def disconnect(self):
        self.ftp.close()
