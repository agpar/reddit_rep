"""Feature extraction tools that operate on a Comment (tree) structure"""

import math
import numpy as np


def tree_size(comment):
    if len(comment.children) > 0:
        return sum([(1 + c.st_stats.size) for c in comment.children])
    else:
        return 0


def tree_depth(comment):
    if len(comment.children) > 0:
        return 1 + max([c.st_stats.depth for c in comment.children])
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

    avg = comment.st_stats.avg_score
    if not avg:
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
    if comment.st_stats.size == 0:
        return None
    return subtree_features.controversial_count / comment.st_stats.size
