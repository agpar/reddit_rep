import psycopg2
from comment import Comment
from settings import settings
conn = psycopg2.connect(**settings["DB"])


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


def get_by_id(comment_id):
    query = f"""
    SELECT * FROM comments c
    WHERE c.id = '{comment_id}'
    """
    cursor = conn.cursor()
    cursor.execute(query)
    return Comment(row_to_dict(cursor, cursor.fetchone()))

def get_parents(already_seen=set()):
    """Get all comments with at least one child.

    Sample comment data set has 579_402
    """
    already_seen_str = [f"{x}" for x in already_seen]
    already_seen_str = "'{}'".format("','".join(already_seen))
    seen_query = f"id not in ({already_seen_str}) and" if already_seen else ""
    query = f"""
        SELECT * FROM comments
        WHERE
        {seen_query}
        't1_' || id in (
            SELECT parent_id
            FROM comments
        );
        """
    cursor = conn.cursor()
    cursor.execute(query)
    return cursor


def get_multi_parents(already_seen=set(), min_children=2):
    """Only parents with at least some amount of children.

    Sample comment data-set has 622_727 with 2.
    """
    already_seen_str = [f"{x}" for x in already_seen]
    already_seen_str = "'{}'".format("','".join(already_seen))
    seen_query = f"id not in ({already_seen_str}) and" if already_seen else ""

    query = f"""
        SELECT * FROM comments c1
        WHERE
        {seen_query}
        't1_' || c1.id in (
            SELECT parent_id
            FROM comments c2
            group by c2.parent_id
            having count(*) >= 2
        );
    """
    cursor = conn.cursor()
    cursor.execute(query)
    return cursor

def get_parents_child_and_depth(already_seen=set(), min_children=2):
    """Get parents with at least min_children and at least depth 2.

    Sample comments has 480_146
    """
    already_seen_str = [f"{x}" for x in already_seen]
    already_seen_str = "'{}'".format("','".join(already_seen))
    seen_query = f"id not in ({already_seen_str}) and" if already_seen else ""

    query = f"""
        SELECT c1.id FROM comments c1
        WHERE
        {seen_query}
        't1_' || c1.id in (
            SELECT parent_id
            FROM comments c2
            group by c2.parent_id
            having count(*) >= {min_children}
        )
        and
        't1_' || c1.id in (
            SELECT parent_id
            FROM comments c2
            where 't1_' || c2.id in (SELECT parent_id FROM comments)
        );
    """
    cursor = conn.cursor()
    cursor.execute(query)
    return cursor

def get_children_of(comment_id):
    """Get all children of a comment"""
    if not comment_id.startswith("t1_"):
        comment_id = "t1_" + comment_id

    query = f"""
        SELECT * FROM comments
        WHERE parent_id = '{comment_id}';
        """
    cursor = conn.cursor()
    cursor.execute(query)
    return cursor
