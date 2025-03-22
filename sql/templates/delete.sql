-- Delete a user
DELETE FROM users WHERE uid = '';

-- Delete a user's email
DELETE FROM user_email WHERE uid = '' AND email = '';

-- Delete a follow relationship
DELETE FROM follows WHERE follower_uid = '' AND followee_uid = '';

-- Delete a platform
DELETE FROM platform WHERE pid = '';

-- Delete a video game
DELETE FROM video_games WHERE vid = '';

-- Delete a genre
DELETE FROM genre WHERE gid = '';

-- Delete a relationship between a video game and a genre
DELETE FROM video_game_genre WHERE vid = '' AND gid = '';

-- Delete a contributor
DELETE FROM contributor WHERE dpid = '';

-- Delete a video game publisher relationship
DELETE FROM video_game_publisher WHERE dpid = '' AND vid = '';

-- Delete a video game developer relationship
DELETE FROM video_game_developer WHERE dpid = '' AND vid = '';

-- Delete a video game from a platform
DELETE FROM video_game_platforms WHERE pid = '' AND vid = '';

-- Delete a user's rating for a video game
DELETE FROM user_rating WHERE uid = '' AND vid = '';

-- Delete a user's play session
DELETE FROM user_plays WHERE uid = '' AND vid = '' AND start = '';

-- Delete a collection
DELETE FROM collection WHERE cid = '';

-- Delete a user's ownership of a collection
DELETE FROM user_has_collection WHERE uid = '' AND cid = '';

-- Delete a video game from a collection
DELETE FROM collection_has_video_game WHERE cid = '' AND vid = '';

-- Delete a user's platform association
DELETE FROM user_platform WHERE uid = '' AND pid = '';

-- Delete all video games associated with the PS3 or Playstation 3 platform
DELETE FROM video_games
WHERE vid IN (
    SELECT DISTINCT vg.vid
    FROM video_games vg
    JOIN video_game_platforms vgp ON vg.vid = vgp.vid
    JOIN platform p ON vgp.pid = p.pid
    WHERE p.name IN ('PS3', 'Playstation 3')
);
