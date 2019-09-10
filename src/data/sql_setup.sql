CREATE TABLE comments(
	id VARCHAR(20) PRIMARY KEY,
	author VARCHAR(100),
	score INT,
	subreddit_id VARCHAR(20),
	gilded INT,
	stickied boolean,
	retrieved_on INT,
	created_utc INT,
	link_id VARCHAR(20),
	controversiality INT,
	parent_id VARCHAR(20),
	subreddit VARCHAR(100),
	body TEXT
);

\copy comments FROM '/home/alex/comments.csv' DELIMITER ',' CSV HEADER QUOTE '"'

CREATE INDEX subreddits ON Comments(subreddit);
CREATE INDEX parents on COMMENTS(parent_id);
