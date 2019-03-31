from mongo_query import load_comments
from trees import build_trees
from settings import settings
import logging


def printif(string):
    if settings['SHOW_PROGRESS']:
        print(string)


def load():
    printif("loading comments...")
    comments = load_comments()
    printif("building trees...")
    trees = build_trees(comments)
    nonempty_trees = [(c, stf) for c,stf in trees if c.children]
    return comments, trees, nonempty_trees