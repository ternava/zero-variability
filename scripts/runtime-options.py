#!/usr/bin/env python3
"""Finds runtime options"""

import re
import subprocess
import os
import argparse
import csv

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
stats_file = "./measures/options.csv"

def nr_runtime_options(exe_file):
    p = subprocess.run([exe_file, "--help"],
                       stdout=subprocess.PIPE,
                       stderr=subprocess.STDOUT)
    nr_of_loc = p.stdout.decode('ascii')
    _, tail = os.path.split(exe_file)
    return tail, nr_of_loc


def main():

    directory = get_args().path

    f = open(stats_file, "w")
    writer = csv.writer(f)
    header = ['Utility', "Nr_options", 'RT_options']
    writer.writerow(header)
    
    
    for file in os.listdir(directory):
        # Find only the executable files
        fn = os.path.join(directory, file)
        # "extract-magic" is a file in perl, 
        # it doesn't have an extension either (!)
        if os.path.isfile(fn) and file != "extract-magic":
            match = re.search("^[^.]+$", file)

            if match:
                print(file)
                output = nr_runtime_options(fn)
                # Find the long run-time options that start with "--"
                r_long = re.compile(r"[-]+\w+")
                #r_short = re.compile(r"(\w*(\-)\w*)")
                mat = r_long.findall(output[1])
                print(mat)
                print(len(set(mat)))
                writer.writerow((file, len(set(mat)), mat))
                
                """ct_options = [x[0] for x in mat]
                print([x for x in ct_options])
                print(len(ct_options))
                """
    f.close()


if __name__ == "__main__":
    main()
