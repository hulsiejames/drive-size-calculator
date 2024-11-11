# -*- coding: utf-8 -*-
"""
Purpose: Given a drive path, walks the drive and returns the size of all
           files within the drive

         Intended to assist with network drive management

"""

# # # # IMPORTS # # # # 
# Built-Ins
import os
import pathlib
import time
import logging
# Third Party
from datetime import datetime
# Local Imports

# # # # CONSTANTS # # # #
# Path to crawl and return size of
DRIVE_PATH = pathlib.Path(r"M:\\")
# Drive path as filename
CLEAN_DRIVE_PATH = str(DRIVE_PATH).replace(r":", "-").replace("\\", "-").replace("--", "-")

# Directory to store log file
LOGGING_OUTPUT_DIR = pathlib.Path(os.getcwd()) / "logs"
# Filename for output log file
LOGGING_FILENAME = f"drive_size_calculator_{datetime.now().strftime('%H_%M_%S___%d-%m-%y')}.log"

LOGGING_FILENAME = f"drive_size_calc_on_{CLEAN_DRIVE_PATH}_{datetime.now().strftime('%H_%M_%S___%d-%m-%y')}.log"

# Number of bytes in one MB
MB_THRESH = 2**2
# Number of bytes in one GB
GB_THRESH = 2**30

# # # # CLASSES # # # # 

class Timer:
    """
    Class to keep track of run times
    """

    def __init__(self):
        """initialises timer"""
        self.start_time = time.time()
        self.step_start_time = self.start_time

    def elapsed_time(self):
        """returns total elapsed time"""
        return time.time() - self.start_time

    def elapsed_step_time(self):
        """returns step time since last self.reset_set_timer()"""
        return time.time() - self.step_start_time

    def reset_step_timer(self):
        """resets the current `step_start_time` to be current time"""
        self.step_start_time = time.time()

# # # # FUNCTIONS # # # #


def format_total_time(
    seconds: float, 
    ) -> str:
    """
    Formats total time in seconds and returns string
    """

    mins, secs = divmod(seconds, 60)

    if mins > 60:
        # At least an hour
        hours, secs = divmod(seconds, 60**2)
        mins, secs = divmod(secs, 60)
        
        return f"Process completed in: {int(hours)} Hours, {int(mins)}.{round(((secs/60)*100))} Minutes."

    elif mins > 0:
        # Under an hour

        return f"Process completed in: {int(mins)} Minutes, {round(secs, 2)} Minutes."


def commence_logging(
    logging_output_path: pathlib.Path,
) -> logging.Logger:
    """
    Function to commence stream & file logging, returns stream logger
    """

    if not os.path.isdir(logging_output_path.parent):
        os.makedirs(logging_output_path.parent)

    LOGGER_MSG_FMT_STR = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    LOGGER_DATE_FMT_STR = "%Y-%m-%d %H:%M:%S"

    # Create a logger object
    log = logging.getLogger(__name__)
    log.setLevel(logging.INFO)

    # Remove all handlers associated with the logger object (avoid duplicated logging)
    for handler in log.handlers[:]:
        log.removeHandler(handler)

    # Create formatter
    formatter = logging.Formatter(fmt=LOGGER_MSG_FMT_STR, datefmt=LOGGER_DATE_FMT_STR)

    # Create handlers
    file_handler = logging.FileHandler(logging_output_path)
    file_handler.setLevel(logging.DEBUG)

    stream_handler = logging.StreamHandler()
    stream_handler.setLevel(logging.INFO)

    # Apply formatting to handlers
    file_handler.setFormatter(formatter)
    stream_handler.setFormatter(formatter)

    # Add handlers to logger object
    log.addHandler(file_handler)
    log.addHandler(stream_handler)

    return log


def bytes_to_mb(
        bytes_size: int,
) -> int:
    """
    Calculates size in Mb from bytes
    """
    return bytes_size / (1024 ** 2)


def bytes_to_gb(
        bytes_size: int,
) -> int:
    """
    Calculates size in Gb from bytes
    """
    return bytes_size / (1024 ** 3)


def bytes_to_kb(
    bytes_size: int,
) -> int:
    """
    Calculates size in Kb from bytes
    """
    return bytes_size / 1024


def get_directory_size(
        dir_path: pathlib.Path,
) -> int:
    """
    Function to return the size of all files contained within a directory.

    Applies os.walk to will assess files in all sub directories of passed directory.
    """
    total_size = 0
    total_dirs = 0
    all_dirs = set()
    timer.reset_step_timer()
    for dirs, _, __ in os.walk(dir_path):
        all_dirs.add(dirs)
        total_dirs += 1

    LOG.info("About to walk process %s directories within %s",
             total_dirs,
             dir_path,
             )
    LOG.debug("About to walk %s contained within %s",
              all_dirs,
              dir_path,
              )

    LOG.info("(it took %s seconds to find the dirs to walk above)",
             round(timer.elapsed_step_time(), 4),
             )
    timer.reset_step_timer()

    internal_timer = Timer()
    for path, _, filenames in os.walk(dir_path):
        for filename in filenames:
            filepath = os.path.join(path, filename)
            if os.path.exists(filepath):

                LOG.debug("Reading: %s\%s", path, filename)

                total_size += os.path.getsize(filepath)

    LOG.info("Total size of %s and sub-dirs calculated in %s seconds as %s Mb",
             dir_path,
             round(internal_timer.elapsed_step_time(), 4),
             bytes_to_mb(total_size),
             )

    return total_size


# =============================================================================
# def get_directory_size(
#         dir_path: pathlib.Path,
# ) -> Generator[Tuple[pathlib.Path, int], None, None]:
#     """
#     Function to yield the size of all files contained within each sub-directory of dir_path.
# 
#     Applies os.walk to assess files in all sub directories of passed directory.
#     """
#     for dirpath, dirnames, filenames in os.walk(dir_path):
#         total_size = 0
#         for filename in filenames:
#             filepath = os.path.join(dirpath, filename)
#             if os.path.exists(filepath):
#                 total_size += os.path.getsize(filepath)
#         yield pathlib.Path(dirpath), total_size
# =============================================================================


def find_network_drive_sizes(
        network_drive: pathlib.Path,
) -> dict:
    """
    Calculates the size of each directory contained within a network directory
    """

    directory_sizes = {}

    for item in os.listdir(network_drive):
        itempath = os.path.join(network_drive, item)
        if os.path.isdir(itempath):
            directory_sizes[itempath] = get_directory_size(itempath)

    return directory_sizes


# =============================================================================
# def find_network_drive_sizes(
#         network_drive: pathlib.Path,
# ) -> dict:
#     """
#     Calculates the size of each directory and sub-directory contained within a network directory
#     """
#     
#     directory_sizes = {}
#     
#     for item in os.listdir(network_drive):
#         itempath = os.path.join(network_drive, item)
#         if os.path.isdir(itempath):
#             for dirpath, size in get_directory_size(itempath):
#                 directory_sizes[dirpath] = size
#     
#     return directory_sizes
# =============================================================================


# # # # PROCESS # # # #

# Initialise the loggers
LOGGER_OUT_PATH = pathlib.Path(LOGGING_OUTPUT_DIR) / LOGGING_FILENAME
LOG = commence_logging(logging_output_path=LOGGER_OUT_PATH)

# Initialise the timer
timer = Timer()

sizes = find_network_drive_sizes(DRIVE_PATH)

LOG.info("Converting sizes to GB")
sizes_gb = {key: round(bytes_to_gb(value), 4) for key, value in sizes.items()}
LOG.info("Converting sizes to MB")
sizes_mb = {key: round(bytes_to_mb(value), 4) for key, value in sizes.items()}

for directory, size in sizes.items():
    if size >= GB_THRESH:
        LOG.info(
            "Directory: %s Size: %s GB",
            directory,
            round(bytes_to_gb(size), 4),
            )
        continue
    
    if MB_THRESH <= size <= GB_THRESH:
        LOG.info(
            "Directory: %s Size: %s MB",
            directory,
            round(bytes_to_mb(size), 4),
            )
        continue

    # Must be in Kb then
    LOG.info(
        "Directory: %s Size: %s",
        directory,
        round(bytes_to_kb(size), 4),
    )

LOG.info("Drive %s has size %s GB",
         DRIVE_PATH,
         bytes_to_gb(sum(sizes.values())))

formatted_time = format_total_time(timer.elapsed_time())
LOG.info("%s", formatted_time)

print("Export results?")