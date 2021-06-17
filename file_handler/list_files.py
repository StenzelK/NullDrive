import os
from pprint import pprint

from NullDrive import settings

MAX_DIR =  1 * 1024 ** 3

def list_files(username):
    path = 'media/userfiles/{}'.format(username)

    filepaths = []

    for dirname, dirnames, filenames in os.walk(path):

        for filename in filenames:
            # print(os.path.join(dirname, filename))
            filepaths.append(filename)


    return filepaths


def get_dir_size(path):
    total_size = 0

    for dirpath, dirnames, filenames in os.walk(path):
        for f in filenames:
            fp = os.path.join(dirpath, f)
            total_size += os.path.getsize(fp)

    # print(total_size <= max_size)
    return total_size

def check_dir_size(path):

    return get_dir_size(path) <= MAX_DIR


def check_file_size(file):
    max_size = 1 * 1024 ** 2  # 500MB
    statinfo = os.stat(file)

    return statinfo.st_size <= max_size


def secure_delete(username, filename, passes=1):

    path = 'media/userfiles/{}/{}'.format(username, filename)
    with open(path, "ba+") as delfile:
        length = delfile.tell()
        for i in range(passes):
            delfile.seek(0)
            delfile.write(os.urandom(length))
    os.remove(path)


