from pymongo import MongoClient
from collections import defaultdict
from typing import List

from trees import build_trees, print_tree
from comment import Comment, SubtreeStats
from feature_extraction import SubtreeFeatures

MONGOURL = "mongodb://127.0.0.1:27017/?gssapiServiceName=mongodb"
client = MongoClient(MONGOURL)
comments_db = client.reddit.sampleComments

DATA_SIZE = 50_000


def load_all(cursor):
    """Pull everything a cursor returns into memory"""
    docs = []
    for doc in cursor[:DATA_SIZE]:
        docs.append(doc)
    return docs


def load_comments(comments_db):
    """Get all comments from the given db into memory"""
    cursor = comments_db.find({})
    docs = load_all(cursor)
    return [Comment(d) for d in docs]


def interactive():
    comments = load_comments(comments_db)
    trees = build_trees(comments)
    return comments, trees


comments, trees = interactive()
nonempty_trees = [(c, stf) for c,stf in trees if c.children]
