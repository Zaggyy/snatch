from services.log.Logger import Logger
import os
import yaml


class Config():

    def __init__(self, file_path):
        self.logger = Logger('config')
        self.file_path = file_path
        self.config = {}

    def read_config(self):
        self.logger.info(f'Config file path: {self.file_path}')
        # Check if the file exists
        if not os.path.isfile(self.file_path):
            self.logger.error(f'File not found: {self.file_path}')
            raise FileNotFoundError()

        # Read the YAML file
        with open(self.file_path, 'r') as stream:
            try:
                self.config = yaml.load(stream, Loader=yaml.SafeLoader)
                self.logger.success(f'Config file read: {self.file_path}')
            except yaml.YAMLError as exc:
                self.logger.error(
                    f'Error while reading the config file: {exc}')
                raise Exception()

    def validate(self):
        # Validate the YAML config
        if not self.config:
            self.logger.error('Config file is empty.')
            raise Exception()
        if not 'ftp' in self.config:
            self.logger.error('Missing FTP configuration.')
            raise Exception()
        if not 'host' in self.config['ftp']:
            self.logger.error('Missing FTP host.')
            raise Exception()
        if not 'user' in self.config['ftp']:
            self.logger.error('Missing FTP user.')
            raise Exception()
        if not 'password' in self.config['ftp']:
            self.logger.error('Missing FTP password.')
            raise Exception()
        if not 'remote_dir' in self.config['ftp']:
            self.logger.error('Missing FTP remote directory.')
            raise Exception()
        if not 'chunk_size' in self.config['ftp']:
            self.logger.error('Missing download chunk size.')
        # Make sure the chunk size is a positive integer
        if not isinstance(self.config['ftp']['chunk_size'], int) or self.config['ftp']['chunk_size'] < 1:
            self.logger.error('Invalid chunk size.')
            raise Exception()

        self.logger.success(f'Config file is valid.')
