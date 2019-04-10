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
    stats.update(multi(c, lambda x: x.stats['sent'], 'sent'))
    stats.update(multi(c, lambda x: x.stats['punc_ques'], 'punc_ques'))
    stats.update(multi(c, lambda x: x.stats['punc_excl'], 'punc_excl'))
    stats.update(multi(c, lambda x: x.stats['punc_per'], 'punc_per'))
    stats.update(multi(c, lambda x: x.stats['punc'], 'punc'))
    stats.update(multi(c, lambda x: x.stats['profanity'], 'profanity'))
    stats.update(multi(c, lambda x: x.stats['hate_count'], 'hate_count'))
    stats.update(multi(c, lambda x: x.stats['hate_conf'], 'hate_conf'))
    stats.update(multi(c, lambda x: x.stats['off_conf'], 'off_conf'))

    stats['child_score_disag'] = child_disagreement(c)
    stats['child_contro'] = child_contro(c)
    stats['child_deleted'] = child_deleted(c)

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

def child_contro(comment):
    if len(comment.children) == 0:
        return None
    child_contro = [c.stats['controversial'] for c in comment.children]
    pos = [s for s in child_contro if s]
    return len(pos) / len(child_contro)

def child_deleted(comment):
    if len(comment.children) == 0:
        return None
    child_deleted = [c.stats['is_deleted'] for c in comment.children]
    pos = [s for s in child_deleted if s]
    return len(pos) / len(child_deleted)