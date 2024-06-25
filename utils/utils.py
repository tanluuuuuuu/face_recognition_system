import yaml
from yaml.loader import SafeLoader

def open_file_cfg(config_path) -> dict:
    with open(config_path) as f:
        file_cfg = yaml.load(f, Loader=SafeLoader)
    return file_cfg