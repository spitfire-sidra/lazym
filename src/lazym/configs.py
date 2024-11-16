import configparser
from pathlib import Path

from .constants import DEFAULT_TEMPERATURE


def load_config():
    config = configparser.ConfigParser()
    config_path = Path.home() / '.config' / 'lazym' / 'config.ini'
    default_config = {
        'DEFAULT': {
            'model': 'llama3.1:8b',
            'message_format': 'lowercase',  # lowercase, sentence case
            'temperature': DEFAULT_TEMPERATURE,
            'prompt': '',
            'rstrip_period': 'true',
        }
    }
    
    if config_path.exists():
        config.read(config_path)
    else:
        config.read_dict(default_config)
    return config['DEFAULT']


configurations = load_config()
