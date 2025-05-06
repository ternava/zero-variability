#!/usr/bin/env python3
"""calculates the binary size
of the GNU core utilities, in bytes"""

import os
import csv
import re
import argparse


def get_args():
    """get command-line arguments"""

    parser = argparse.ArgumentParser(
        description="For input directory",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter)

    parser.add_argument('--path', type=dir_path)

    return parser.parse_args()


def dir_path(path):
    if os.path.isdir(path):
        return path
    else:
        raise argparse.ArgumentTypeError(
            f"{path} is not a valid path. Should be /your/path/coreutil/src/")


# You may need to create a "measures" directory
stats_file = "./measures/BinarySize.csv"


def binary_size(exe_name):
    exe_stats = os.stat(exe_name)
    #print(exe_stats)
    exe_size = exe_stats.st_size
    return os.path.basename(exe_name), exe_size


def main():

    directory = get_args().path

    f = open(stats_file, "w")
    writer = csv.writer(f)
    header = ['Utility', "BinarySize"]
    writer.writerow(header)

    for file in os.listdir(directory):
        match = re.search("^[^.]+$", file)

        if match:
            fn = os.path.join(directory, file)
            bs = binary_size(fn)
            print(bs)
            writer.writerow(bs)
    f.close()

if __name__ == "__main__":
    main()
