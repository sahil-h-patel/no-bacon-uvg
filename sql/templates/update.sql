-- Update a user's username and password
UPDATE users
SET username = '', password = ''
WHERE uid = '';

-- Update a user's email address
UPDATE user_email
SET email = ''
WHERE uid = '' AND email = '';

-- Update a follow relationship
UPDATE follows
SET follower_uid = '', followee_uid = ''
WHERE followee_uid = '' AND follower_uid = '';

-- Update a platform name
UPDATE platform
SET name = ''
WHERE pid = '';

-- Update a video game's title and ESRB rating
UPDATE video_games
SET title = '', esrb = ''
WHERE vid = '';

-- Update a genre name
UPDATE genre
SET genre = ''
WHERE gid = '';

-- Update a contributor's name
UPDATE contributor
SET name = ''
WHERE dpid = '';

-- Update a video game's price, release date, and platform
UPDATE video_game_platforms
SET price = '', release_date = ''
WHERE pid = '' AND vid = '';

-- Update a user's rating for a video game
UPDATE user_rating
SET rating = ''
WHERE uid = '' AND vid = '';

-- Update a user's play session start and end times
UPDATE user_plays
SET start = '', end_time = ''
WHERE uid = '' AND vid = '' AND start = '';

-- Update a collection's name
UPDATE collection
SET name = ''
WHERE cid = '';

-- Update the relationship between a user and a collection
UPDATE user_has_collection
SET cid = ''
WHERE uid = '' AND cid = '';

-- Update the relationship between a collection and a video game
UPDATE collection_has_video_game
SET vid = ''
WHERE cid = '' AND vid = '';

-- Update the relationship between a user and a platform
UPDATE user_platform
SET pid = ''
WHERE uid = '' AND pid = '';
