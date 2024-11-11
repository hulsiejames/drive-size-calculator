# -*- coding: utf-8 -*-
"""
Created on Fri Nov  8 12:14:22 2024

@author: Signalis

THIS FUNTION RETURNS A MORE DEAILED PATH ANALYSIS

"""

import os
import pathlib
from typing import Generator, Tuple

def get_directory_size(
        dir_path: pathlib.Path,
) -> Generator[Tuple[pathlib.Path, int], None, None]:
    """
    Function to yield the size of all files contained within each sub-directory of dir_path.

    Applies os.walk to assess files in all sub directories of passed directory.
    """
    for dirpath, dirnames, filenames in os.walk(dir_path):
        total_size = 0
        for filename in filenames:
            filepath = os.path.join(dirpath, filename)
            if os.path.exists(filepath):
                total_size += os.path.getsize(filepath)
        yield pathlib.Path(dirpath), total_size

def find_network_drive_sizes(
        network_drive: pathlib.Path,
) -> dict:
    """
    Calculates the size of each directory and sub-directory contained within a network directory
    """
    directory_sizes = {}
    for item in os.listdir(network_drive):
        itempath = os.path.join(network_drive, item)
        if os.path.isdir(itempath):
            for dirpath, size in get_directory_size(itempath):
                directory_sizes[dirpath] = size
    return directory_sizes

# Example usage:
network_drive = pathlib.Path(r"Y:\PBA\Analysis")  # Replace with your network drive path
sizes = find_network_drive_sizes(network_drive)
for directory, size in sizes.items():
    print(f"Directory: {directory} Size: {size / (1024 ** 2):.2f} MB")
