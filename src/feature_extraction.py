"""Feature extraction tools that operate on a Comment (tree) structure"""

import math
import numpy as np

class SubtreeFeatures:
    """Stores features of a subtree to help with recursive feautre building."""

    def __init__(self):
        self.scores = []
        self.controversial_count = 0

    @staticmethod
    def combine(subtree_features_list):
        """Returns a new instance with properties of all in given list."""
        combined = SubtreeFeatures()

        for stf in subtree_features_list:
            combined.scores.extend(stf.scores)
            combined.controversial_count += stf.controversial_count

        return combined

    def update(self, comment):
        """Updates this instance with the features from the given comment."""
        self.scores.append(comment.score)
        self.controversial_count += comment.controversial


def tree_size(comment):
    if len(comment.children) > 0:
        return sum([(1 + c.stats.size) for c in comment.children])
    else:
        return 0

def tree_depth(comment):
    if len(comment.children) > 0:
        return 1 + max([c.stats.depth for c in comment.children])
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

    avg = comment.stats.avg_score
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
    if comment.stats.size == 0:
        return None
    return subtree_features.controversial_count / comment.stats.size
