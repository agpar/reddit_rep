"""Feature extraction tools that operate on a Comment (tree) structure"""

import math
import numpy as np
from comment import CommentFeatures

def compute_subtree_metadata_features(c, stf):
    c.st_stats = CommentFeatures()
    stats = c.st_stats

    stats['desc_size'] = tree_size(c)
    stats['desc_depth'] = tree_depth(c)
    stats['desc_contro'] = percent_controversial(c,stf)
    stats['desc_score_disag'] = disagreement(c,stf)

    stats.update(multi(stf, lambda x: x.scores, 'score'))


def _avg(stf, selector):
    data = selector(stf)
    data = [d for d in data if d is not None]
    if not data:
        return None

    return np.mean(data)


def _std(stf, selector):
    data = selector(stf)
    data = [d for d in data if d is not None]
    if not data:
        return None

    return np.std(data)


def _min(stf, selector):
    data = selector(stf)
    data = [d for d in data if d is not None]
    if not data:
        return None

    return min(data)


def _max(stf, selector):
    data = selector(stf)
    data = [d for d in data if d is not None]
    if not data:
        return None

    return min(data)

def _median(stf, selector):
    data = selector(stf)
    data = [d for d in data if d is not None]
    if not data:
        return None

    data.sort()
    return data[int(len(data)/2)]


def multi(stf, selector, label):
    agg_funcs = [_avg, _std, _min, _max, _median]
    agg_labs = ['avg', 'std', 'min', 'max', 'med']
    features = []
    for fn, fn_name in zip(agg_funcs, agg_labs):
        feat_label = f"desc_{fn_name}_{label}"
        features.append((feat_label, fn(stf,selector)))
    return features


def tree_size(comment):
    if len(comment.children) > 0:
        return sum([(1 + c.st_stats['desc_size']) for c in comment.children])
    else:
        return 0


def tree_depth(comment):
    if len(comment.children) > 0:
        return 1 + max([c.st_stats['desc_depth'] for c in comment.children])
    else:
        return 0


def percent_controversial(comment, subtree_features):
    if comment.st_stats['desc_size'] == 0:
        return None
    return subtree_features.controversial_count / comment.st_stats['desc_size']


def disagreement(comment, stf):
    if len(stf.scores) == 0:
        return None
    if len(stf.scores) < 2:
        return 0.0

    neg_scores = [s for s in stf.scores if s < 1]
    pos_scores = [s for s in stf.scores if s > 1]
    if len(pos_scores) == 0:
        return 1.0

    return len(neg_scores)/len(pos_scores)
