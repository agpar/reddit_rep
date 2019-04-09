import sqlite3
from comment import Comment
conn = sqlite3.connect("./data/reddit_comments")


def row_to_dict(cursor, row):
    d = {}
    for i, col in enumerate(cursor.description):
        d[col[0]] = row[i]
    return d


def get_one(cursor) -> Comment:
    row = cursor.fetchone()
    if row is None:
        raise IndexError
    d = row_to_dict(cursor, row)
    return Comment(d)


def get_all(cursor):
    rows = cursor.fetchall()
    dicts = [row_to_dict(cursor, row) for row in rows]
    return [Comment(d) for d in dicts]


def comment_iter(cursor):
    while True:
        row = cursor.fetchone()
        if row is None:
            cursor.close()
            raise StopIteration

        d = row_to_dict(cursor, row)
        yield Comment(d)


def get_parents() -> sqlite3.Cursor:
    """Get all comments with at least one child.

    Sample comment data set has 579_402
    """
    query = """
        SELECT * FROM comments
        WHERE "t1_" || id in (
            SELECT parent_id
            FROM comments
        );
        """
    cursor = conn.execute(query)
    return cursor


def get_multi_parents() -> sqlite3.Cursor:
    """Only parents with at least 2 children.

    Sample comment data-set has 160_901
    """
    query = """
        SELECT * FROM comments
        WHERE "t1_" || id in (
            SELECT parent_id
            FROM comments
            group by parent_id
            HAVING count(*) >=2
        );
    """
    cursor = conn.execute(query)
    return cursor


def get_children_of(comment_id) -> sqlite3.Cursor:
    """Get all children of a comment"""
    if not comment_id.startswith("t1_"):
        comment_id = "t1_" + comment_id

    query = f"""
        SELECT * FROM comments
        WHERE parent_id == '{comment_id}';
        """
    cursor = conn.execute(query)
    return cursor
