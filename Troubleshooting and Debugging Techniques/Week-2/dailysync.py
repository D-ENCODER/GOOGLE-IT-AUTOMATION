#!/usr/bin/env python
import subprocess
from multiprocessing import Pool
import os

global src
src = "{}/data/prod/".format(os.getenv("HOME"))


def sync_data(folder):
    dest = "{}/data/prod_backup/".format(os.getenv("HOME"))
    subprocess.call(["rsync", "-arq", folder, dest])
    print("Handling {}".format(folder))


if __name__ == "__main__":
    folders = []
    root = next(os.walk(src))[0]
    dirs = next(os.walk(src))[1]

    for dir in dirs:
        folders.append(os.path.join(root, dir))

    pool = Pool(len(folders)) if len(folders) != 0 else Pool(1)
    pool.map(sync_data, folders)
