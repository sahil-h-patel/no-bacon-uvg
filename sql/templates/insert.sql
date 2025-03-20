-- Insert a new user
INSERT INTO users (username, password, first_name, last_name, creation_date, last_access)
VALUES ('', '', '', '', '', '');

-- Insert a new email for a user
INSERT INTO user_email (uid, email)
VALUES ('', '');

-- Insert a new follow relationship
INSERT INTO follows (follower_uid, followee_uid)
VALUES ('', '');

-- Insert a new platform
INSERT INTO platform (name)
VALUES ('');

-- Insert a new video game
INSERT INTO video_games (title, esrb)
VALUES ('', '');

-- Insert a new genre
INSERT INTO genre (genre)
VALUES ('');

-- Insert a relationship between a video game and a genre
INSERT INTO video_game_genre (vid, gid)
VALUES ('', '');

-- Insert a new contributor
INSERT INTO contributor (name)
VALUES ('');

-- Insert a new video game publisher relationship
INSERT INTO video_game_publisher (dpid, vid)
VALUES ('', '');

-- Insert a new video game developer relationship
INSERT INTO video_game_developer (dpid, vid)
VALUES ('', '');

-- Insert a video game into a platform with price and release date
INSERT INTO video_game_platforms (pid, vid, price, release_date)
VALUES ('', '', '', '');

-- Insert a user's rating for a video game
INSERT INTO user_rating (uid, vid, rating)
VALUES ('', '', '');

-- Insert a new play session for a user
INSERT INTO user_plays (uid, vid, start, end_time)
VALUES ('', '', '', '');

-- Insert a new collection
INSERT INTO collection (name)
VALUES ('');

-- Insert a user's ownership of a collection
INSERT INTO user_has_collection (uid, cid)
VALUES ('', '');

-- Insert a video game into a collection
INSERT INTO collection_has_video_game (cid, vid)
VALUES ('', '');

-- Insert a user's association with a platform
INSERT INTO user_platform (uid, pid)
VALUES ('', '');
