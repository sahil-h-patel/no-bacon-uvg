-- Delete a user by their UID
DELETE FROM users WHERE uid = '';

-- Delete a specific email for a user
DELETE FROM user_email WHERE uid = '' AND email = '';

-- Delete a follow relationship
DELETE FROM follows WHERE follower_uid = '' AND followee_uid = '';

-- Delete a platform by its PID
DELETE FROM platform WHERE pid = '';

-- Delete a video game by its VID
DELETE FROM video_games WHERE vid = '';

-- Delete a genre by its GID
DELETE FROM genre WHERE gid = '';

-- Delete a video game genre relation
DELETE FROM video_game_genre WHERE vid = '' AND gid = '';

-- Delete a contributor by their DPID
DELETE FROM contributor WHERE dpid = '';

-- Delete a publisher relationship for a video game
DELETE FROM video_game_publisher WHERE dpid = '' AND vid = '';

-- Delete a developer relationship for a video game
DELETE FROM video_game_developer WHERE dpid = '' AND vid = '';

-- Delete a video game platform relation
DELETE FROM video_game_platforms WHERE pid = '' AND vid = '';

-- Delete a user rating for a video game
DELETE FROM user_rating WHERE uid = '' AND vid = '' AND rating = '';

-- Delete a user's play session for a video game
DELETE FROM user_plays WHERE uid = '' AND vid = '' AND start = '';

-- Delete a collection by its CID
DELETE FROM collection WHERE cid = '';

-- Delete a collection owned by a user
DELETE FROM user_has_collection WHERE uid = '' AND cid = '';

-- Delete a video game from a collection
DELETE FROM collection_has_video_game WHERE cid = '' AND vid = '';

-- Delete a platform owned by a user
DELETE FROM user_platform WHERE uid = '' AND pid = '';
