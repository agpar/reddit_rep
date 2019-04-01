"""Feature extraction tools that operate on a Comment (tree) structure"""

import math
import numpy as np
from comment import CommentFeatures

def compute_subtree_metadata_features(c, stf):
    c.st_stats = CommentFeatures()
    stats = c.st_stats

    stats['size'] = tree_size(c)
    stats['depth'] = tree_depth(c)
    stats['avg_score'] = average_score(c,stf)
    stats['std_score'] = std_dev_score(c,stf)
    stats['min_score'] = min_score(stf)
    stats['max_score'] = max_score(stf)
    stats['contr_score'] = percent_controversial(c,stf)

def tree_size(comment):
    if len(comment.children) > 0:
        return sum([(1 + c.st_stats['size']) for c in comment.children])
    else:
        return 0


def tree_depth(comment):
    if len(comment.children) > 0:
        return 1 + max([c.st_stats['depth'] for c in comment.children])
    else:
        return 0


def average_score(comment, subtree_features):
    """Average score of discussion, does not include root"""
    if not subtree_features.scores:
        return None
    return np.mean(subtree_features.scores)


def std_dev_score(comment, subtree_features):
    """Std dev of score of discussion, does not include root"""
    if not subtree_features.scores:
        return None

    return np.std(subtree_features.scores)


def min_score(subtree_features):
    if not subtree_features.scores:
        return None
    return min(subtree_features.scores)


def max_score(subtree_features):
    if not subtree_features.scores:
        return None
    return max(subtree_features.scores)


def percent_controversial(comment, subtree_features):
    if comment.st_stats['size'] == 0:
        return None
    return subtree_features.controversial_count / comment.st_stats['size']
