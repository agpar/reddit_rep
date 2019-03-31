from pymongo import MongoClient

from comment import Comment

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


def load_comments(comments_db=comments_db):
    """Get all comments from the given db into memory"""
    cursor = comments_db.find({})
    docs = load_all(cursor)
    return [Comment(d) for d in docs]
