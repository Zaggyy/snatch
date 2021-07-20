from constants.constants import SCRIPT_VERSION
from services.config.Config import Config
from services.ftp.ftp import Connection
from services.log.Logger import Logger
import argparse
import tempfile
import threading
import shutil

from utils.utils import chunk

# Parse the arguments
parser = argparse.ArgumentParser(
    description='Multi-threaded parallel FTP download script.')
parser.add_argument('-v', '--version', action='version',
                    version=SCRIPT_VERSION)
parser.add_argument(
    '--config', help='path to the configuration file', required=True)
parser.add_argument('--zip', action='store_true',
                    help='should the files be zipped after download')

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
    logger.info("Created {} chunks.".format(len(file_chunks)))
    # Create a random temporary directory
    tmp_dir = tempfile.mkdtemp()
    # Create a thread for each chunk and start it immediately
    for chunk_index, chunk in enumerate(file_chunks):
        logger.info("Starting thread {} of {}.".format(chunk_index + 1,
                                                        len(file_chunks)))
        ftp = Connection(config.config['ftp'], chunk_index + 1)
        # Create a thread
        thread = threading.Thread(target=lambda: ftp.download(chunk, tmp_dir), daemon=True)
        # Start the thread
        thread.start()
    # Wait for all threads to finish
    for thread in threading.enumerate():
        if thread is not threading.currentThread():
            thread.join()
    logger.divider()
    logger.info("Downloaded all files to {}".format(tmp_dir))
    # Zip the directory if necessary
    if args.zip:
        logger.info("Zipping files")
        archive = config.config['ftp']['remote_dir'].replace('/', '_')
        shutil.make_archive(archive, 'zip', tmp_dir)
        logger.success("Zipped files to {}".format(archive + '.zip'))
        # Delete the temporary directory
        shutil.rmtree(tmp_dir)
except:
    logger.error("An error has occurred. Exiting.")
