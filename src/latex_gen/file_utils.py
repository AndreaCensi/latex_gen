import os

__all__ = ["make_sure_dir_exists"]


def make_sure_dir_exists(d):
    if not os.path.exists(d):
        os.makedirs(d)
