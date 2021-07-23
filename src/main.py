from constants.constants import SCRIPT_VERSION
from services.config.Config import Config
from services.ftp.ftp import Connection
from services.log.Logger import Logger
from utils.utils import chunk

import argparse
import tempfile
import threading
import multiprocessing
import shutil
import os

# Parse the arguments
parser = argparse.ArgumentParser(
    description='Multi-threaded parallel FTP download script.')
parser.add_argument('-v', '--version', action='version',
                    version=SCRIPT_VERSION)
parser.add_argument(
    '--config', help='path to the configuration file', required=True)
parser.add_argument('--zip', action='store_true',
                    help='should the files be zipped after download')
parser.add_argument('--process', action='store_true',
                    help='use multiple processes instead of threads')
parser.add_argument('--output', help='set output directory')

args = parser.parse_args()

# Start the main thread
logger = Logger('main')

logger.info("snatch v{}".format(SCRIPT_VERSION))
logger.divider()

try:
    # Load configuration
    config = Config(args.config)
    config.read_config()
    config.validate()
    logger.divider()
    # Get the file listing
    ftp = Connection(config.config['ftp'])
    files = ftp.traverse(config.config['ftp']['remote_dir'])
    ftp.disconnect()
    # Create multiple chunks
    file_chunks = chunk(files, config.config['ftp']['chunk_size'])
    logger.divider()
    logger.info("Downloading {} files.".format(len(files)))
    logger.info("Creating {} processes.".format(len(file_chunks)))
    # Create a random temporary directory
    tmp_dir = tempfile.mkdtemp() if args.output is None else args.output

    Process = multiprocessing.Process if args.process else threading.Thread

    # Create a process for each chunk and start it immediately
    processes = []
    for chunk_index, chunk in enumerate(file_chunks):
        logger.info("Starting process {} of {}.".format(chunk_index + 1,
                                                        len(file_chunks)))
        ftp = Connection(config.config['ftp'], chunk_index + 1)
        # Create a process
        process = Process(target=lambda: ftp.download(chunk, tmp_dir))
        processes.append(process)
        # Start the process
        process.start()

    for process in processes:
        process.join()

    logger.divider()
    logger.info("Downloaded all files to {}".format(tmp_dir))
    # Zip the directory if necessary
    if args.zip:
        logger.info("Zipping files")
        # Get the archive name
        archive_name = os.path.join(tmp_dir, os.path.basename(
            config.config['ftp']['remote_dir'])) if args.output is not None else os.path.basename(config.config['ftp']['remote_dir'])

        shutil.make_archive(archive_name, 'zip', tmp_dir)
        logger.success("Zipped files to {}".format(archive_name + '.zip'))
        # Get the removal path
        removal_path = os.path.join(tmp_dir, config.config['ftp']['remote_dir'].split(
            os.path.sep)[0]) if args.output is not None else tmp_dir
        shutil.rmtree(removal_path)
except:
    logger.error("An error has occurred. Exiting.")
