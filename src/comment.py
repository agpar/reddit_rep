class Comment:
    def __init__(self, data):
        if not data:
            raise Exception("Need a full data dict.")
        self._data = data

        self.children = []
        self.stats = SubtreeStats()

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

        # Includes the node itself, for recursion reasons
        self.size = 1
        self.depth = 0

        # Score based features
        self.avg_score = None
        self.std_dev_score = None
        self.min_score = None
        self.max_score = None

        # controversiality based
        self.percent_controversial = None
