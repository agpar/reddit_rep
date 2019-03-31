"""Feature extraction tools that operate on a Comment (tree) structure"""

import math
from typing import List

import nltk
from comment import Comment


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
    return 1 + sum([c.stats.size for c in comment.children])


def tree_depth(comment):
    if len(comment.children) > 0:
        return 1 + max([c.stats.depth for c in comment.children])
    else:
        return 0


def average_score(comment, subtree_features):
    """Average score of discussion, does not include root"""
    if not subtree_features.scores:
        return None
    # (comment.tree_size - 1) to exclude root.
    return sum(subtree_features.scores) / (comment.stats.size - 1)


def std_dev_score(comment, subtree_features):
    """Std dev of score of discussion, does not include root"""
    if not subtree_features.scores:
        return None

    avg = comment.stats.avg_score
    if not avg:
        return None

    return math.sqrt(sum(pow(s - avg, 2) for s in subtree_features.scores))


def min_score(subtree_features):
    if not subtree_features.scores:
        return None
    return min(subtree_features.scores)


def max_score(subtree_features):
    if not subtree_features.scores:
        return None
    return max(subtree_features.scores)


def percent_controversial(comment, subtree_features):
    if comment.stats.size == 1:
        return None
    return subtree_features.controversial_count / (comment.stats.size - 1)
