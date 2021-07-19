import yaml

# Read a YML file and return the data as a dictionary
def read_yml_config(path):
    try:
        with open(path, 'r') as f:
            return yaml.load(f, Loader=yaml.SafeLoader)
    except FileNotFoundError:
        print("File not found: {}".format(path))
        return None