from collections import defaultdict
from tqdm import tqdm

import feature_extraction as FE
from comment import Comment
from feature_extraction import SubtreeComments
from feature_extraction import compute_child_features
from feature_extraction import compute_nl_features
from feature_extraction import compute_subtree_metadata_features
from settings import settings
from sql_query import get_parents, get_all, comment_iter, get_children_of, get_parents_child_and_depth, get_by_id


def GenerateTrees(already_seen=set(), min_children=2):
    """Build up all trees using a generator style"""
    root_cursor = get_parents_child_and_depth(set(), min_children)
    all_ids = root_cursor.fetchall()
    new_ids = set([x[0] for x in all_ids]) - already_seen
    assert(len(new_ids) == len(all_ids) - len(already_seen))
    for new_id in new_ids:
        root = get_by_id(new_id)
        tree_root, tree_features = _generate_rec_tree(root)
        yield tree_root


def _generate_rec_tree(root):
    subtree_featues = []
    child_curs = get_children_of(root.comment_id)
    children = get_all(child_curs)
    child_curs.close()
    for child in children:
        subtree, features = _generate_rec_tree(child)
        subtree_featues.append(features)
        root.children.append(subtree)

    combined_features = SubtreeComments.combine(subtree_featues)
    _compute_features(root, combined_features)
    combined_features.update(root)
    return root, combined_features



def build_trees(comments):
    """Build discussion trees for the given set comments"""
    by_parent = defaultdict(list)
    for c in comments:
        by_parent[c.parent_id].append(c)

    trees = []
    roots = [c for c in comments if c.parent_type == 'link']
    if settings['SHOW_PROGRESS']:
        roots = tqdm(roots)
    for c in roots:
        tree_root, tree_features = _build_rec_tree(c, by_parent)
        trees.append((tree_root, tree_features))

    return trees


def _build_rec_tree(c: Comment, by_parent) -> (Comment, SubtreeComments):
    subtree_featues = []
    for child in by_parent[c.comment_id]:
        subtree, features = _build_rec_tree(child, by_parent)
        subtree_featues.append(features)
        c.children.append(subtree)

    combined_features = SubtreeComments.combine(subtree_featues)
    _compute_features(c, combined_features)

    combined_features.update(c)
    return c, combined_features


def _compute_features(c: Comment, subtree_features: SubtreeComments):
    """Computes an associates aggregate features of this subtree"""

    # subtree features
    compute_subtree_metadata_features(c, subtree_features)

    # Children stats
    compute_child_features(c)

    # Natural language stats
    compute_nl_features(c)


def print_tree(c: Comment, indent=0):
    indents = f"{indent} - "
    print(indents + c.body)
    for c in c.children:
        print_tree(c, indent=indent + 2)