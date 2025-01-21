import pickle as pkl
from pathlib import Path


def read_pkl_file(path: Path):
    if path.exists():
        return pkl.load(open(path, "rb"))
    else:
        return None


def dump_pkl_file(path: Path, data):
    pkl.dump(data, open(path, "wb"))
