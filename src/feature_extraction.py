"""Feature extraction tools that operate on a Node (tree) structure"""

import math
from typing import List

import nltk
from comment import Node


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

    def update(self, node):
        """Updates this instance with the features from the given node."""
        self.scores.append(node.comment.score)
        self.controversial_count += node.comment.controversial


def tree_size(node):
    return 1 + sum([c.stats.size for c in node.children])


def tree_depth(node):
    if len(node.children) > 0:
        return 1 + max([c.stats.depth for c in node.children])
    else:
        return 0


def average_score(node, subtree_features):
    """Average score of discussion, does not include root"""
    if not subtree_features.scores:
        return None
    # (node.tree_size - 1) to exclude root.
    return sum(subtree_features.scores) / (node.stats.size - 1)


def std_dev_score(node, subtree_features):
    """Std dev of score of discussion, does not include root"""
    if not subtree_features.scores:
        return None

    avg = node.stats.avg_score
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


def percent_controversial(node, subtree_features):
    if node.stats.size == 1:
        return None
    return subtree_features.controversial_count / (node.stats.size - 1)
