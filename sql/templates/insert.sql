-- users
INSERT INTO users (Username, Password, Firstname, Lastname, CreationDate, LastAccess) 
VALUES ('', '', '', '', '', '');

-- user_email
INSERT INTO user_email (uid, email) 
VALUES ('', '');

-- follows
INSERT INTO follows (follower_uid, followee_uid) 
VALUES ('', '');

-- platform
INSERT INTO platform (name) 
VALUES ('');

-- video_games
INSERT INTO video_games (ESRB, Title) 
VALUES ('', '');

-- genre
INSERT INTO genre (genre) 
VALUES ('');

-- video_game_genre
INSERT INTO video_game_genre (vid, gid) 
VALUES ('', '');

-- contributor
INSERT INTO contributor (name) 
VALUES ('');

-- video_game_publisher
INSERT INTO video_game_publisher (dpid, vid) 
VALUES ('', '');

-- video_game_developer
INSERT INTO video_game_developer (dpid, vid) 
VALUES ('', '');

-- video_game_platforms
INSERT INTO video_game_platforms (pid, vid, price, release_date) 
VALUES ('', '', '', '');

-- user_rating
INSERT INTO user_rating (uid, vid, rating) 
VALUES ('', '', '');

-- user_plays
INSERT INTO user_plays (uid, vid, start, end_time) 
VALUES ('', '', '', '');

-- collection
INSERT INTO collection (name) 
VALUES ('');

-- user_has_collection
INSERT INTO user_has_collection (uid, cid) 
VALUES ('', '');

-- collection_has_video_game
INSERT INTO collection_has_video_game (cid, vid) 
VALUES ('', '');

-- user_platform
INSERT INTO user_platform (uid, pid) 
VALUES ('', '');
