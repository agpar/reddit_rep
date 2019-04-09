from trees import build_trees
from settings import settings
import numpy as np

VECTOR_FILE = "./data/vectors.csv"

def printif(string):
    if settings['SHOW_PROGRESS']:
        print(string)

def load_vectors():
    with open(VECTOR_FILE, 'r') as f:
        header = f.__next__().split(",")
        data = []
        for line in f:
            import pdb
            pdb.set_trace()
            data.append(np.array([float(f) for f in line.split(",")[1:]]))
    return header, np.array(data)

def load():
    printif("loading comments...")
    comments = load_comments()
    printif("building trees...")
    trees = build_trees(comments)
    nonempty_trees = [(c, stf) for c,stf in trees if c.children]
    return comments, trees, nonempty_trees