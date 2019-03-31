class SubtreeFeatures:
    """Stores features of a subtree to help with recursive feautre building."""

    def __init__(self):
        self.scores = []
        self.controversial_count = 0

    @staticmethod
    def combine(subtree_features_list):
        """Returns a new instance with properties of all in given list."""
        combined = SubtreeFeatures()

        for stf in subtree_features_list:
            combined.scores.extend(stf.scores)
            combined.controversial_count += stf.controversial_count

        return combined

    def update(self, comment):
        """Updates this instance with the features from the given comment."""
        self.scores.append(comment.score)
        self.controversial_count += comment.controversial