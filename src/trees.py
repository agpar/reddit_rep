from collections import defaultdict
from tqdm import tqdm

import feature_extraction as FE
from comment import Comment
from feature_extraction import SubtreeFeatures
from settings import SHOW_PROGRESS


def build_trees(comments):
    """Build discussion trees for the given set comments"""
    by_parent = defaultdict(list)
    for c in comments:
        by_parent[c.parent_id].append(c)

    trees = []
    roots = [c for c in comments if c.parent_type == 'link']
    if SHOW_PROGRESS:
        roots = tqdm(roots)
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
    st_stats = c.st_stats

    # Tree dimension features
    st_stats.size = FE.tree_size(c)
    st_stats.depth = FE.tree_depth(c)

    # Score based features
    st_stats.avg_score = FE.average_score(c, subtree_features)
    st_stats.std_dev_score = FE.std_dev_score(c, subtree_features)
    st_stats.min_score = FE.min_score(subtree_features)
    st_stats.max_score = FE.max_score(subtree_features)

    # Controversiality
    st_stats.percent_controversial = FE.percent_controversial(c,
                                                           subtree_features)

    stats = c.stats
    stats.word_count = FE.word_count(c)
    stats.prp_first = FE.percent_first_pronouns(c)
    stats.prp_second = FE.percent_second_pronouns(c)
    stats.prp_third = FE.percent_third_pronouns(c)


def print_tree(c: Comment, indent=0):
    indents = f"{indent} - "
    print(indents + c.body)
    for c in c.children:
        print_tree(c, indent=indent + 2)