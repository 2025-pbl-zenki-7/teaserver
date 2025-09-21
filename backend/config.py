import toml

import os
import toml


def get_tea_config():
    config_path = os.path.join(os.path.dirname(__file__), '..', 'config.toml')
    with open(config_path, 'r') as f:
        return toml.load(f)['teas']


def get_arduino_config():
    config_path = os.path.join(os.path.dirname(__file__), '..', 'config.toml')
    with open(config_path, 'r') as f:
        return toml.load(f)['arduino']


def save_tea_config(config):
    config_path = os.path.join(os.path.dirname(__file__), '..', 'config.toml')
    with open(config_path, 'r') as f:
        full_config = toml.load(f)
    full_config['teas'] = config['teas']
    with open(config_path, 'w') as f:
        toml.dump(full_config, f)
