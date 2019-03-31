from mongo_query import load_comments
from trees import build_trees


def reload():
    comments = load_comments()
    trees = build_trees(comments)
    nonempty_trees = [(c, stf) for c,stf in trees if c.children]
    return comments, trees, nonempty_trees

comments, trees, nonempty_trees = reload()