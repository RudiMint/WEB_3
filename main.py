"""
Sort files
"""
import argparse
import logging

from pathlib import Path
from shutil import copyfile
from threading import Thread, Condition
from queue import Queue

"""
--source [-s]
--output [-o] default folder = dist
"""

parser = argparse.ArgumentParser(description="Sorting folder")
parser.add_argument("--source", "-s", help="Source folder", default="picture")
parser.add_argument("--output", "-o", help="Output folder", default="dist")

# print(parser.parse_args())
args = vars(parser.parse_args())
# print(args)

source = Path(args.get("source"))
output = Path(args.get("output"))
scanning_completed = False


def th_grabs_folder(path: Path):
    grabs_folder(path)
    global scanning_completed
    with condition:
        logging.debug(f"Notify all")
        scanning_completed = True
        condition.notify_all()
def grabs_folder(path: Path) -> None:
    logging.debug(f"Grabs folder {path}")
    for el in path.iterdir():
        if el.is_dir():
            folders.put(el)
            grabs_folder(el)


def copy_file() -> None:
    logging.debug(f"Wait...")
    with condition:
        # while not scanning_completed:
        condition.wait()
    while True:
        if folders.empty():
            break
        folder = folders.get()
        logging.debug(f"Handling folder {folder}")
        for el in folder.iterdir():
            if el.is_file():
                ext = el.suffix[1:]
                new_folder = output / ext
                try:
                    new_folder.mkdir(parents=True, exist_ok=True)
                    copyfile(el, new_folder / el.name)
                except OSError as err:
                    logging.error(err)


if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG, format="%(threadName)s %(message)s")
    condition = Condition()
    folders = Queue()

    folders.put(source)

    th_grabs = Thread(target=th_grabs_folder, args=(source, ))
    th_grabs.start()

    # th_grabs.join()
    threads = []
    for i in range(2):
        th = Thread(target=copy_file, name=f"Thread#{i}")
        th.start()
        threads.append(th)

    [th.join() for th in threads]

    print("you may delete folder")

