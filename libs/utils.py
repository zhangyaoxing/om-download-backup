from pathlib import Path
from shutil import rmtree, move
import glob
import os
import json
import logging
import argparse
import tarfile
import io

config = None
def load_config():
    global config
    if config == None:
        config = json.load(open("./config.json"))
        config["public_key"] = config.get("public_key", os.environ.get("public_key", None))
        config["private_key"] = config.get("private_key", os.environ.get("private_key", None))
        if config["public_key"] == None or config["private_key"] == None:
            logging.error("Public/private keys are not configured.")
            exit()
        config["api_base_url"] = f'{config["om_url"]}{"" if config["om_url"].endswith("/") else "/"}api/public/v1.0'
    return config

levels = logging._nameToLevel
parser = argparse.ArgumentParser(description="Barclays POC")
parser.add_argument("--logLevel",
    help = "Set log level.",
    choices= ["INFO", "DEBUG", "WARNING", "ERROR", "CRITICAL"],
    default = "INFO")
args = parser.parse_args()
log_level = levels[args.logLevel]
logging.basicConfig(level = log_level)
def get_logger(name):
    logger = logging.getLogger(name)
    return logger
