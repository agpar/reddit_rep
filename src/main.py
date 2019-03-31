from mongo_query import load_comments
from trees import build_trees
from settings import *
import logging

def printif(string):
    if SHOW_PROGRESS:
        print(string)

def reload():
    printif("loading comments...")
    comments = load_comments()
    printif("building trees...")
    trees = build_trees(comments)
    nonempty_trees = [(c, stf) for c,stf in trees if c.children]
    return comments, trees, nonempty_trees

comments, trees, nonempty_trees = reload()