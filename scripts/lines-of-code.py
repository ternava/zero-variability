#!/usr/bin/env python3
"""calculates the LoC in each of the GNU 
core utilities, for .c and .h files"""

import os
import subprocess
import csv
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
stats_file = "./measures/LoC.csv"


def nr_lines_of_code(c_file):
    p = subprocess.run(["cloc", c_file],
                       stdout=subprocess.PIPE,
                       stderr=subprocess.STDOUT)
    nr_of_loc = p.stdout.decode('ascii').split()[-2]
    _, tail = os.path.split(c_file)
    return tail, nr_of_loc


def count_ch_loc(dir, dict_ch):
    for filename in os.listdir(dir):
        name = os.path.splitext(filename)[0]
        fn = os.path.join(dir, filename)
        if filename.endswith(".c"):
            loc = nr_lines_of_code(fn)
            # print(loc[0], loc[1])
            dict_ch[name] = loc[1]
        elif filename.endswith(".h") and name in dict_ch:
            # Check if type of value of key is list or not
            if not isinstance(dict_ch[name], list):
                # If type is not list then make it list
                dict_ch[name] = [dict_ch[name]]
                # count its lines of code
                loc_h = nr_lines_of_code(fn)
                # print(loc_h[0], loc_h[1])
                # Append the value in list
                dict_ch[name].append(loc_h[1])


def main():

    directory = get_args().path
    dict_ch = {}

    f = open(stats_file, "w")
    writer = csv.writer(f)
    header = ["Utility", "LoC"]
    writer.writerow(header)

    count_ch_loc(directory, dict_ch)

    for key in dict_ch:
        print(key, "->", dict_ch[key])

        if isinstance(dict_ch[key], list) and key != "coreutils":
            int_values = list(map(int, dict_ch[key]))
            writer.writerow((key, sum(int_values)))
        else:
            writer.writerow((key, dict_ch[key]))

    f.close()


if __name__ == "__main__":
    main()
