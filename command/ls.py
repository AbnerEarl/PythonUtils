import argparse
import datetime
from pathlib import Path

parser = argparse.ArgumentParser(prog="ls", description="list files", add_help=True)
parser.add_argument("path", nargs="?", default=".", help="file path")
parser.add_argument("-l", "--list", action="store_true", help="use a long listing format")
parser.add_argument("-a", "--all", action="store_true", help="show all files")
parser.add_argument("-r", "--reverse", action="store_true", help="sort files by name")
modes = list("rwx" * 3)
# parser.print_help()
# print("------")
args = parser.parse_args()


# print(args)
# print(args.l, args.path)


def list_file(path, detail=False, all=False, reverse=False):
    p = Path(path)
    for f in sorted(p.iterdir(), reverse=reverse):
        if not all and f.name.startswith("."):
            continue

        st = f.stat()
        if detail:
            dt = datetime.datetime.fromtimestamp(st.st_mtime).strftime("%Y-%m-%d %H:%M:%S")
            print(_get_mode(st.st_mode), f.owner(), f.group(), _get_size(st.st_size), _get_type(f), dt, f.name)
        else:
            print(f.name)


def _get_mode(mode):
    m = ""
    for i, x in enumerate("{:09b}".format(mode)[-9:]):
        m += modes[i] if x == "1" else "-"
    return m


def _get_type(path):
    if path.is_dir():
        return "d"
    elif path.is_symlink():
        return "l"
    elif path.is_socket():
        return "s"
    elif path.is_char_device():
        return "c"
    elif path.is_block_device():
        return "b"
    else:
        return "-"


def _get_size(size):
    units = ["B", "K", "M", "G", "T", "P"]
    index = 0
    length = len(units)
    while size >= 1000 and index + 1 < length:
        size = size // 1000
        index += 1
    return "{}{}".format(size, units[index])


list_file(args.path, args.list, args.all, args.reverse)
