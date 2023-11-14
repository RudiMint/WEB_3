"""
Sort files (homework)
"""
import argparse
import logging
import sys

from pathlib import Path
from shutil import copyfile
from multiprocessing import Pool, cpu_count

"""
--source [-s]
--output [-o] default folder = dist
"""

parser = argparse.ArgumentParser(description="Sorting folder")
parser.add_argument("--source", "-s", help="Source folder", required=True)
parser.add_argument("--output", "-o", help="Output folder", default="dist")

print(parser.parse_args())
args = vars(parser.parse_args())
print(args)

source = Path(args.get("source"))
output = Path(args.get("output"))


def grabs_folder(path: Path) -> list:
    folders = []
    for el in path.iterdir():
        if el.is_dir():
            folders.append(el)
            inner_dir = grabs_folder(el)
            if len(inner_dir):
                folders += inner_dir
    return folders


def copy_file(path: Path) -> None:
    for el in path.iterdir():
        if el.is_file():
            ext = el.suffix[1:]
            new_folder = output / ext
            try:
                new_folder.mkdir(parents=True, exist_ok=True)
                copyfile(el, new_folder / el.name)
            except OSError as err:
                logging.error(err)
                sys.exit(1)


if __name__ == "__main__":
    logging.basicConfig(level=logging.ERROR, format="%(threadName)s %(message)s")

    folders_list = [source, *grabs_folder(source)]
    with Pool(cpu_count()) as pool:
        pool.map(copy_file, folders_list)
        pool.close()
        pool.join()
    print("you may delete folder")

