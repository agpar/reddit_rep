from comment import Comment

c1 = {
    'gilded': 0,
    'stickied': False,
    'author_flair_css_class': None,
    'ups': 66,
    'author': 'a1',
    'score': 66,
    'subreddit_id': 't5_movies',
    'parent_id': 't3_abc',
    'edited': False,
    'controversiality': 0,
    'author_flair_text': None,
    'id': 'abc1',
    'body': 'root comment',
    'subreddit': 'movies',
    'created_utc': 1451606588,
    'retrieved_on': 1454207987,
    'distinguished': None,
    'link_id': 't3_abc'}

c2 = {
    'author_flair_text': None,
    'controversiality': 0,
    'edited': False,
    'parent_id': 't1_abc1',
    'body': 'child 1',
    'subreddit': 'movies',
    'id': 'abc1.1',
    'created_utc': 1451606653,
    'distinguished': None,
    'retrieved_on': 1454208003,
    'link_id': 't3_abc',
    'stickied': False,
    'gilded': 0,
    'author_flair_css_class': None,
    'ups': 6,
    'author': 'a2',
    'score': 6,
    'subreddit_id': 't5_movies'}

c3 = {
    'author_flair_text': None,
    'controversiality': 0,
    'edited': False,
    'parent_id': 't1_abc1',
    'body': 'child 2',
    'subreddit': 'movies',
    'id': 'abc1.2',
    'created_utc': 1451606653,
    'distinguished': None,
    'retrieved_on': 1454208003,
    'link_id': 't3_abc',
    'stickied': False,
    'gilded': 0,
    'author_flair_css_class': None,
    'ups': 3,
    'author': 'a3',
    'score': 3,
    'subreddit_id': 't5_movies'}

c4 = {
    'author_flair_text': None,
    'controversiality': 1,
    'edited': False,
    'parent_id': 't1_abc1.2',
    'body': 'child 2.1',
    'subreddit': 'movies',
    'id': 'abc1.2.1',
    'created_utc': 1451606653,
    'distinguished': None,
    'retrieved_on': 1454208003,
    'link_id': 't3_abc',
    'stickied': False,
    'gilded': 0,
    'author_flair_css_class': None,
    'ups': -4,
    'author': 'a4',
    'score': -4,
    'subreddit_id': 't5_movies'}


test_comments = {
    'comment_data': [c1, c2, c3, c4],
    'size': 3,
    'depth': 2,
    'avg_score': 1.666_666_666,
    'std_dev_score': 4.189_935_029,
    'max_score': 6,
    'min_score': -4,
    'percent_contro': 1/3

}
