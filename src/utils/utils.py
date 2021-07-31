import tempfile
import os
import uuid

# Create a chunk of an array of specified size


def chunk(arr, size):
    return [arr[i:i + size] for i in range(0, len(arr), size)]

# Return output directory depending on the configuration


def get_output_dir(config):
    if 'local' in config and 'output_dir' in config['local']:
        if os.path.exists(config['local']['output_dir']):
            return config['local']['output_dir']
    return tempfile.mkdtemp()

# Return archive name depending on the configuration


def get_archive_name(config):
    if 'local' in config and 'archive_name' in config['local']:
        return config['local']['archive_name']
    elif 'local' in config and 'output_dir' in config['local']:
        path = os.path.basename(config['local']['output_dir'])
        if len(path) > 0:
            return path
    return str(uuid.uuid4())
