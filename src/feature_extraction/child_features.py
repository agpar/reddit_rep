"""
Features averaged over the direct children of a comment.
"""
import numpy as np

def compute_child_features(comment):
    comment.ch_stats.avg_score = avg_child_score(comment)
    comment.ch_stats.std_score = std_child_score(comment)


def _avg(comment, selector):
    if not comment.children:
        return None

    return np.mean([selector(c) for c in comment.children])


def _std(comment, selector):
    if not comment.children:
        return None

    return np.std([selector(c) for c in comment.children])


def avg_child_score(comment):
    return _avg(comment, lambda c: c.score)


def std_child_score(comment):
    return _std(comment, lambda c: c.score)