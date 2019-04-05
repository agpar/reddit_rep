"""
Features averaged over the direct children of a comment.
"""
from collections import Counter
import numpy as np
from comment import CommentFeatures

def compute_child_features(c):
    c.ch_stats = CommentFeatures()
    stats = c.ch_stats

    stats.update(multi(c, lambda x: x.score, 'score'))
    stats.update(multi(c, lambda x: x.stats['prp_first'], 'prp_first'))
    stats.update(multi(c, lambda x: x.stats['prp_second'], 'prp_second'))
    stats.update(multi(c, lambda x: x.stats['prp_third'], 'prp_third'))

    stats['disagreement'] = child_disagreement(c)

def _avg(comment, selector):
    data = [selector(c) for c in comment.children]
    data = [d for d in data if d is not None]
    if not data:
        return None

    return np.mean(data)


def _std(comment, selector):
    data = [selector(c) for c in comment.children]
    data = [d for d in data if d is not None]
    if not data:
        return None

    return np.std(data)


def _min(comment, selector):
    data = [selector(c) for c in comment.children]
    data = [d for d in data if d is not None]
    if not data:
        return None

    return min(data)


def _max(comment, selector):
    data = [selector(c) for c in comment.children]
    data = [d for d in data if d is not None]
    if not data:
        return None

    return min(data)

def _median(comment, selector):
    data = [selector(c) for c in comment.children]
    data = [d for d in data if d is not None]
    if not data:
        return None

    data.sort()
    return data[int(len(data)/2)]



def multi(comment, selector, label):
    agg_funcs = [_avg, _std, _min, _max, _median]
    agg_labs = ['avg', 'std', 'min', 'max', 'med']
    features = []
    for fn, fn_name in zip(agg_funcs, agg_labs):
        feat_label = f"child_{fn_name}_{label}"
        features.append((feat_label, fn(comment,selector)))
    return features


def child_disagreement(comment):
    if len(comment.children) == 0:
        return None
    if len(comment.children) < 2:
        return 0.0

    child_scores = [c.score for c in comment.children]
    neg_scores = [s for s in child_scores if s < 1]
    pos_scores = [s for s in child_scores if s > 1]
    if len(pos_scores) == 0:
        return 1.0

    return len(neg_scores)/len(pos_scores)