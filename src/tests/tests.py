from unittest import TestCase

from comment import Comment
from trees import build_trees
from tests.test_data import test_comments as data
from settings import settings

settings['SHOW_PROGRESS'] = False


class TestSubtreeStats(TestCase):

    def setUp(self):
        self.comments = [Comment(c) for c in data['comment_data']]
        self.tree, self.stf = build_trees(self.comments)[0]
        self.stats = self.tree.st_stats

    def test_size(self):
        self.assertEqual(self.stats.size, data['size'])

    def test_depth(self):
        self.assertEqual(self.stats.depth, data['depth'])

    def test_avg_score(self):
        self.assertAlmostEqual(self.stats.avg_score, data['avg_score'])

    def test_std_dev_score(self):
        self.assertAlmostEqual(self.stats.std_dev_score, data['std_dev_score'])

    def test_min_score(self):
        self.assertEqual(self.stats.min_score, data['min_score'])

    def test_max_score(self):
        self.assertEqual(self.stats.max_score, data['max_score'])

    def test_percent_contr(self):
        self.assertEqual(self.stats.percent_controversial,
            data['percent_contro'])