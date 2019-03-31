from mongo_query import load_comments
from trees import build_trees


def interactive():
    comments = load_comments()
    trees = build_trees(comments)
    return comments, trees


comments, trees = interactive()
nonempty_trees = [(c, stf) for c,stf in trees if c.children]