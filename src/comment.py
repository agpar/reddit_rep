class Comment:
    def __init__(self, data):
        if not data:
            raise Exception("Need a full data dict.")

        # The original data dict
        self._data = data

        # A list of children - to be filled while constructing trees.
        self.children = []

        # Places to store tokenized/labelled versions of the body.
        self.blob = None

        # Stats about this particular comment
        self.stats = CommentStats()

        # Stats about the subtree rooted at this comment.
        self.st_stats = SubtreeStats()

        # Stats abou    t the direct children of this comment.
        self.ch_stats = ChildStats()

    @property
    def comment_id(self):
        return self._data['id']

    @property
    def parent_id(self):
        return self._data['parent_id'][3:]

    @property
    def sub_id(self):
        return self._data['subreddit_id'][3:]

    @property
    def parent_type(self):
        code = self._data['parent_id'][:2]
        if code == "t1":
            return "comment"
        elif code == "t3":
            return "link"
        elif code == "t4":
            return "message"
        raise Exception("Unknown parent type.")

    @property
    def author(self):
        return self._data['author']

    @property
    def body(self):
        return self._data['body']

    @property
    def score(self):
        return self._data['score']

    @property
    def gilded(self):
        return self._data['gilded']

    @property
    def controversial(self):
        return bool(self._data['controversiality'])


class SubtreeStats():
    def __init__(self):
        self.size = None
        self.depth = None

        # Score based features
        self.avg_score = None
        self.std_dev_score = None
        self.min_score = None
        self.max_score = None

        # controversiality based
        self.percent_controversial = None


class CommentStats():
    def __init__(self):
        # Natural language stats
        self.word_count = None
        self.prp_first = None
        self.prp_second = None
        self.prp_third = None


class ChildStats():
    def __init__(self):
        self.avg_score = None