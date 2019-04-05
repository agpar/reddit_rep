from collections import OrderedDict
import numpy as np

class Comment:
    include_child_stats = True
    include_st_stats = True

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
        self.stats = CommentFeatures()

        # Stats about the subtree rooted at this comment.
        self.st_stats = CommentFeatures()

        # Stats abou    t the direct children of this comment.
        self.ch_stats = CommentFeatures()

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

    def to_vector(self, ch=True, st=True):
        vect = []
        if ch:
            vect.extend(self.ch_stats.to_vector())
        if st:
            vect.extend(self.st_stats.to_vector())
        return vect

    def vector_labels(self, ch=True, st=True):
        vect = []
        if ch:
            vect.extend(self.ch_stats.vector_labels())
        if st:
            vect.extend(self.st_stats.vector_labels())
        return vect

    def to_labelled_vector(self, ch=True, st=True):
        vect = []
        if ch:
            vect.extend(self.ch_stats.to_labelled_vector())
        if st:
            vect.extend(self.st_stats.to_labelled_vector())
        return vect

    def is_valid(self):
        vect = self.to_vector()
        return vect and None not in vect


class CommentFeatures():
    def __init__(self, feats=None):
        if feats is None:
            feats = list()
        self._feats = OrderedDict(feats)

    def __getitem__(self, str_key):
        return self._feats.__getitem__(str_key)

    def __setitem__(self, str_key, value):
        return self._feats.__setitem__(str_key, value)

    def update(self, iter):
        return self._feats.update(iter)

    def get(self, key, d=None):
        return self._feats.get(key, d)

    def to_vector(self):
        return np.array(list(self._feats.values()))

    def vector_labels(self):
        return np.array(list(self._feats.keys()))

    def to_labelled_vector(self):
        return list(zip(self.vector_labels(), self.to_vector()))