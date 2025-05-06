import os
import sys

COREUTILS = ["[" ,"arch" ,"b2sum" ,"base32" ,"base64" ,"basename" ,"basenc"
             ,"cat" ,"chcon" ,"chgrp" ,"chmod" ,"chown" ,"chroot" ,"cksum" ,"comm" ,"cp"
             ,"csplit" ,"cut" ,"date" ,"dd" ,"df" ,"dir" ,"dircolors" ,"dirname" ,"du"
             ,"echo" ,"env" ,"expand" ,"expr" ,"factor" ,"false" ,"fmt" ,"fold" ,"groups"
             ,"head" ,"hostid" ,"hostname" ,"id" ,"install" ,"join" ,"kill" ,"link" ,"ln"
             ,"logname" ,"ls" ,"md5sum" ,"mkdir" ,"mkfifo" ,"mknod" ,"mktemp" ,"mv" ,"nice"
             ,"nl" ,"nohup" ,"nproc" ,"numfmt" ,"od" ,"paste" ,"pathchk" ,"pinky" ,"pr"
             ,"printenv" ,"printf" ,"ptx" ,"pwd" ,"readlink" ,"realpath" ,"rm" ,"rmdir"
             ,"runcon" ,"seq" ,"sha1sum" ,"sha224sum" ,"sha256sum" ,"sha384sum" ,"sha512sum"
             ,"shred" ,"shuf" ,"sleep" ,"sort" ,"split" ,"stat" ,"stdbuf" ,"stty" ,"sum"
             ,"sync" ,"tac" ,"tail" ,"tee" ,"test" ,"timeout" ,"touch" ,"tr" ,"true"
             ,"truncate" ,"tsort" ,"tty" ,"uname" ,"unexpand" ,"uniq" ,"unlink" ,"uptime"
             ,"users" ,"vdir" ,"wc" ,"who" ,"whoami" ,"yes"]

def get_program_name_lines(source):
    prog_name = []
    keep = False
    with open(source, 'r') as s:
        for line in s:
            if line.startswith("#define PROGRAM_NAME")\
               or line.startswith("# define PROGRAM_NAME"):
                prog_name.append(line)
                if line.endswith("\\\n"):
                    keep = True
            elif keep:
                prog_name.append(line)
            if line == '\n':
                keep = False

    return prog_name


def clean_list(lines):
    return "".join(map(lambda x: x.strip(), lines))


def get_alternative_names(source):
    prog_name = get_program_name_lines(source)
    merged = clean_list(prog_name)
    return merged.split('"')[1::2]


def dict2graphviz(d):
    s = "digraph G {\n"
    for k, v in d.items():
        for e in v:
            s += f"\"{k}\" -> \"{e}\";\n"
    return s + '}'

def main():
    curr_dir = sys.argv[1]
    prev_dir = os.getcwd()
    os.chdir(curr_dir)
    p2fd = dict()
    src_files = list(
        filter(
            lambda x: "coreutils" not in x and x.endswith(".c"),
            os.listdir()))
    for program in COREUTILS:
        p2fd[program] = []
        p2fd[program].extend(
            filter(lambda x: x.endswith(f"-{program}.c")
                   or x == program + ".c",
                   src_files))
        for f in src_files:
            if program in get_alternative_names(f):
                if f not in p2fd[program]:
                    p2fd[program].append(f)
    print(dict2graphviz(p2fd))


if __name__ == "__main__":
    main()
