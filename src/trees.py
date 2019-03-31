from collections import defaultdict

import feature_extraction as FE
from comment import Comment
from feature_extraction import SubtreeFeatures


def build_trees(comments):
    """Build discussion trees for the given set comments"""
    by_parent = defaultdict(list)
    for c in comments:
        by_parent[c.parent_id].append(c)

    trees = []
    roots = [c for c in comments if c.parent_type == 'link']
    for c in roots:
        tree_root, tree_features = _build_rec_tree(c, by_parent)
        trees.append((tree_root, tree_features))
    return trees


def _build_rec_tree(c: Comment, by_parent) -> (Comment, SubtreeFeatures):
    subtree_featues = []
    for child in by_parent[c.comment_id]:
        subtree, features = _build_rec_tree(child, by_parent)
        subtree_featues.append(features)
        c.children.append(subtree)

    combined_features = SubtreeFeatures.combine(subtree_featues)
    _compute_features(c, combined_features)

    combined_features.update(c)
    return c, combined_features


def _compute_features(c: Comment, subtree_features: SubtreeFeatures):
    """Computes an associates aggregate features of this subtree"""
    stats = c.stats

    # Tree dimension features
    stats.size = FE.tree_size(c)
    stats.depth = FE.tree_depth(c)

    # Score based features
    stats.avg_score = FE.average_score(c, subtree_features)
    stats.std_dev_score = FE.std_dev_score(c, subtree_features)
    stats.min_score = FE.min_score(subtree_features)
    stats.max_score = FE.max_score(subtree_features)

    # Controversiality
    stats.percent_controversial = FE.percent_controversial(c,
                                                           subtree_features)


def print_tree(c: Comment, indent=0):
    indents = [" " for i in range(indent)]
    print("".join(indents) + c.body)
    for c in c.children:
        print_tree(c, indent=indent + 2)