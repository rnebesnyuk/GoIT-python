import argparse
import logging
from pathlib import Path
from shutil import copyfile
from threading import Thread


"""
python main.py --input -i source folder --output -o destination folder
"""

parser = argparse.ArgumentParser(prog="program to sort files in certain folder")
parser.add_argument("-i", "--input", required=True)
parser.add_argument("-o", "--output", default="sorted")
args = vars(parser.parse_args())
input = str(args.get("input"))
output = str(args.get("output"))

folders = []


def folders_collector(path: Path):
    try:
        for el in path.iterdir():
            if el.is_dir():
                folders.append(el)
                folders_collector(el)
    except OSError as err:
        logging.error(err)


def copy_file(path: Path):
    for el in path.iterdir():
        if el.is_file():
            ext = el.suffix
            new_path = output_folder / ext
            try:
                new_path.mkdir(exist_ok=True, parents=True)
                copyfile(el, new_path / el.name)
            except OSError as er:
                logging.error(er)


if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG, format="%(threadName)s %(message)s")
    input_folder = Path(input)
    output_folder = Path(output)
    folders.append(input_folder)
    folders_collector(input_folder)
    print(folders)
    threads = []
    for folder in folders:
        th = Thread(target=copy_file, args=(folder,))
        th.start()
        threads.append(th)

    [th.join() for th in threads]
    print("Files copied, original folder can be removed")
