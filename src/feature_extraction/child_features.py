"""
Features averaged over the direct children of a comment.
"""
import numpy as np
from comment import CommentFeatures

def compute_child_features(c):
    c.ch_stats = CommentFeatures()
    stats = c.ch_stats

    stats['avg_child_score'] = avg_child_score(c)
    stats['std_child_score'] = std_child_score(c)
    stats['avg_prp_first'] = avg_prp_first(c)
    stats['std_prp_first'] = std_prp_first(c)
    stats['avg_prp_second'] = avg_prp_second(c)
    stats['std_prp_second'] = std_prp_second(c)
    stats['avg_prp_third'] = avg_prp_third(c)
    stats['std_prp_third'] = std_prp_third(c)

def _avg(comment, selector):
    data = [selector(c) for c in comment.children]
    if (not data) or not any(d is not None for d in data):
        return None

    return np.mean([d for d in data if d is not None])


def _std(comment, selector):
    data = [selector(c) for c in comment.children]
    if (not data) or not any(d is not None for d in data):
        return None

    return np.std([d for d in data if d is not None])

def _min(comment, selector):
    data = [selector(c) for c in comment.children]
    if (not data) or not any(d is not None for d in data):
        return None

    return min([d for d in data if d is not None])

def _max(comment, selector):
    data = [selector(c) for c in comment.children]
    if (not data) or not any(d is not None for d in data):
        return None

    return min([d for d in data if d is not None])

def avg_child_score(comment):
    return _avg(comment, lambda c: c.score)

def std_child_score(comment):
    return _std(comment, lambda c: c.score)

def avg_prp_first(comment):
    return _avg(comment, lambda c: c.stats['prp_first'])

def std_prp_first(comment):
    return _std(comment, lambda c: c.stats['prp_first'])

def avg_prp_second(comment):
    return _avg(comment, lambda c: c.stats['prp_second'])

def std_prp_second(comment):
    return _std(comment, lambda c: c.stats['prp_second'])

def avg_prp_third(comment):
    return _avg(comment, lambda c: c.stats['prp_third'])

def std_prp_third(comment):
    return _std(comment, lambda c: c.stats['prp_third'])