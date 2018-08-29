import yaml
import os

# Get configuration from env
# Use default conf if the configuration is not set in env
def get_conf(key):
    try:
        return os.environ[key.upper()]
    except:
        with open('config.yaml') as json_data_file:
            conf = yaml.load(json_data_file)
            return conf[key]