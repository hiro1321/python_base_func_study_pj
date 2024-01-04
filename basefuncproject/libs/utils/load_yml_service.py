import yaml
import sys
import os
from typing import List


def load_yml(key: str):
    """
    top_keyを元にapp.ymlの値を取得する
    """
    with open("./app.yml", "r") as yml:
        yml_dict = yaml.safe_load(yml)

    return yml_dict[key]
