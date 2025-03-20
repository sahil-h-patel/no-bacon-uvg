-- users
UPDATE users
SET Username = '', Password = '', Firstname = '', Lastname = '', CreationDate = '', LastAccess = ''
WHERE uid = '';

-- user_email
UPDATE user_email
SET email = ''
WHERE uid = '' AND email = '';

-- follows
UPDATE follows
SET follower_uid = '', followee_uid = ''
WHERE follower_uid = '' AND followee_uid = '';

-- platform
UPDATE platform
SET name = ''
WHERE pid = '';

-- video_games
UPDATE video_games
SET ESRB = '', Title = ''
WHERE vid = '';

-- genre
UPDATE genre
SET genre = ''
WHERE gid = '';

-- video_game_genre
UPDATE video_game_genre
SET vid = '', gid = ''
WHERE vid = '' AND gid = '';

-- contributor
UPDATE contributor
SET name = ''
WHERE dpid = '';

-- video_game_publisher
UPDATE video_game_publisher
SET dpid = '', vid = ''
WHERE dpid = '' AND vid = '';

-- video_game_developer
UPDATE video_game_developer
SET dpid = '', vid = ''
WHERE dpid = '' AND vid = '';

-- video_game_platforms
UPDATE video_game_platforms
SET pid = '', vid = '', price = '', release_date = ''
WHERE pid = '' AND vid = '';

-- user_rating
UPDATE user_rating
SET uid = '', vid = '', rating = ''
WHERE uid = '' AND vid = '' AND rating = '';

-- user_plays
UPDATE user_plays
SET start = '', end_time = ''
WHERE uid = '' AND vid = '' AND start = '';

-- collection
UPDATE collection
SET name = ''
WHERE cid = '';

-- user_has_collection
UPDATE user_has_collection
SET uid = '', cid = ''
WHERE uid = '' AND cid = '';

-- collection_has_video_game
UPDATE collection_has_video_game
SET cid = '', vid = ''
WHERE cid = '' AND vid = '';

-- user_platform
UPDATE user_platform
SET uid = '', pid = ''
WHERE uid = '' AND pid = '';
