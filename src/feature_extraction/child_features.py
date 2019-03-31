"""
Features averaged over the direct children of a comment.
"""

def avg_child_score(comment):
    if not comment.children:
        return None

    return sum(c.score for c in comment.children) / len(comment.children)