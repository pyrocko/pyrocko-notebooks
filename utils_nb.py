import os
import socket
from pyrocko import util

op = os.path

DATA_DIR = op.join(op.dirname(op.abspath(__file__)), 'data')
os.makedirs(DATA_DIR, exist_ok=True)


class NoInternetConnection(Exception):
    pass


def _download_data(fn, dldir=False):
    fpath = data_file_path(fn)
    if not op.exists(fpath):
        if not have_internet():
            raise NoInternetConnection(
                'need internet access to download data')

        url = 'http://data.pyrocko.org/examples/' + fn
        print('downloading %s' % url)
        if dldir:
            util.download_dir(url, fpath)
        else:
            util.download_file(url, fpath)

    return fpath


def download_dir(fn):
    return _download_data(fn, dldir=True)


def download_file(fn):
    return _download_data(fn)


def data_file_path(fn):
    return op.join(DATA_DIR, fn)


def have_internet():
    try:
        return 0 < len([
            (s.connect(('8.8.8.8', 80)), s.close())
            for s in [socket.socket(socket.AF_INET, socket.SOCK_DGRAM)]])

    except OSError:
        return False
