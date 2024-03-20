# pylint: disable=E
""" Functions to work with environment """
import os
from typing import List

from env import DATA_PATH, project_dir

def get_abspath(*path):
    """ Get the absolute path from this file and add the argument path"""
    return os.path.join(project_dir, *path)


def create_dir(path: str = None) -> None:
    """create_chunk_id_dir function service."""
    if not os.path.exists(path):
        os.mkdir(path)

def check_extension(filename, extensions) -> bool:
    """Check available filename extension"""
    ext = filename.split(".")[-1]
    return ext.lower() in extensions