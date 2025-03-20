-----------------------------------------------------------------
--------------------- user stats --------------------------------
-----------------------------------------------------------------

-- query 1: count the total number of collections owned by each user.
SELECT 
    u.username  as user_name,
    count(uhc.cid)  as total_collections
FROM 
    users u
LEFT JOIN 
    user_has_collection uhc ON u.uid = uhc.uid
GROUP BY 
    u.username
ORDER BY 
    total_collections DESC ;

-- query 2: count the total number of video games in collections owned by each user.
SELECT 
    u.username  as user_name,
    count(chvg.vid)  as total_video_games_in_collections
FROM 
    users u
LEFT JOIN 
    user_has_collection uhc ON u.uid = uhc.uid
LEFT JOIN 
    collection_has_video_game chvg ON uhc.cid = chvg.cid
GROUP BY 
    u.username
ORDER BY 
    total_video_games_in_collections DESC ;

-- query 3: calculate the average number of video games per collection for each user.
SELECT 
    u.username  as user_name,
    avg(collection_video_games.total_games)  as avg_games_per_collection
FROM 
    users u
LEFT JOIN 
    user_has_collection uhc ON u.uid = uhc.uid
LEFT JOIN (
    SELECT 
        chvg.cid,
        count(chvg.vid)  as total_games
    FROM 
        collection_has_video_game chvg
    GROUP BY 
        chvg.cid
)  as collection_video_games ON uhc.cid = collection_video_games.cid
GROUP BY 
    u.username
ORDER BY 
    avg_games_per_collection DESC ;

-- query 4: calculate the total playtime (in hours) for all video games in collections owned by each user.
SELECT 
    u.username  as user_name,
    coalesce(sum(extract(epoch FROM (up.end_time - up.start)) / 3600), 0)  as total_playtime_hours
FROM 
    users u
LEFT JOIN 
    user_has_collection uhc ON u.uid = uhc.uid
LEFT JOIN 
    collection_has_video_game chvg ON uhc.cid = chvg.cid
LEFT JOIN 
    user_plays up ON chvg.vid = up.vid and up.uid = u.uid
GROUP BY 
    u.username
ORDER BY 
    total_playtime_hours DESC ;

-- query 5: find the collection with the most video games for each user.
SELECT 
    u.username  as user_name,
    c.name  as collection_name,
    count(chvg.vid)  as total_video_games
FROM 
    users u
LEFT JOIN 
    user_has_collection uhc ON u.uid = uhc.uid
LEFT JOIN 
    collection c ON uhc.cid = c.cid
LEFT JOIN 
    collection_has_video_game chvg ON c.cid = chvg.cid
GROUP BY 
    u.username, c.name
ORDER BY 
    u.username, total_video_games DESC ;

-----------------------------------------------------------------
--------------------- video game stats --------------------------
-----------------------------------------------------------------

-- query 1: count the total number of video games in the database.
SELECT 
    count(*)  as total_video_games
FROM 
    video_games;

-- query 2: calculate the total price of video games grouped by platform.
SELECT 
    p.name  as platform_name,
    sum(vg_platform.price)  as total_price_of_video_games
FROM 
    video_game_platforms vg_platform
JOIN 
    platform p ON vg_platform.pid = p.pid
GROUP BY 
    p.name
ORDER BY 
    total_price_of_video_games DESC ;

-- query 3: count the number of video games for each genre.
SELECT 
    g.genre  as genre_name,
    count(vg_genre.vid)  as video_game_count
FROM 
    video_game_genre vg_genre
JOIN 
    genre g ON vg_genre.gid = g.gid
GROUP BY 
    g.genre
ORDER BY 
    video_game_count DESC ;

-- query 4: calculate the total playtime (in hours) of video games for each user.
SELECT 
    u.username  as user_name,
    coalesce(sum(extract(epoch FROM (up.end_time - up.start)) / 3600), 0)  as total_playtime_hours
FROM 
    users u
LEFT JOIN 
    user_plays up ON u.uid = up.uid
GROUP BY 
    u.username
ORDER BY 
    total_playtime_hours DESC ;

-- query 5: count the number of video games each user has rated.
SELECT 
    u.username  as user_name,
    count(ur.vid)  as rated_video_games
FROM 
    users u
LEFT JOIN 
    user_rating ur ON u.uid = ur.uid
GROUP BY 
    u.username
ORDER BY 
    rated_video_games DESC ;

-----------------------------------------------------------------
--------------------- publisher/developer stats -----------------
-----------------------------------------------------------------

-- query 1: count the total number of video games published by each publisher.
SELECT 
    c.name  as publisher_name,
    count(vgp.vid)  as total_video_games_published
FROM 
    video_game_publisher vgp
JOIN 
    contributor c ON vgp.dpid = c.dpid
GROUP BY 
    c.name
ORDER BY 
    total_video_games_published DESC ;

-- query 2: count the total number of video games developed by each developer.
SELECT 
    c.name  as developer_name,
    count(vgd.vid)  as total_video_games_developed
FROM 
    video_game_developer vgd
JOIN 
    contributor c ON vgd.dpid = c.dpid
GROUP BY 
    c.name
ORDER BY 
    total_video_games_developed DESC ;

-- query 3: find publishers who have also developed video games, along with counts for publishing and developing.
SELECT 
    c.name  as contributor_name,
    count(distinct vgp.vid)  as total_published,
    count(distinct vgd.vid)  as total_developed
FROM 
    contributor c
LEFT JOIN 
    video_game_publisher vgp ON c.dpid = vgp.dpid
LEFT JOIN 
    video_game_developer vgd ON c.dpid = vgd.dpid
GROUP BY 
    c.name
ORDER BY 
    total_published DESC , total_developed DESC ;

-- query 4: calculate the average number of video games published by publishers.
SELECT 
    avg(published_games.total_published)  as average_games_published
FROM (
    SELECT 
        c.name  as publisher_name,
        count(vgp.vid)  as total_published
    FROM 
        video_game_publisher vgp
    JOIN 
        contributor c ON vgp.dpid = c.dpid
    GROUP BY 
        c.name
)  as published_games;

-- query 5: find the most common esrb rating for games published by each publisher.
SELECT 
    c.name  as publisher_name,
    vg.esrb  as most_common_esrb_rating,
    count(vg.vid)  as game_count
FROM 
    video_game_publisher vgp
JOIN 
    contributor c ON vgp.dpid = c.dpid
JOIN 
    video_games vg ON vgp.vid = vg.vid
GROUP BY 
    c.name, vg.esrb
ORDER BY 
    c.name, game_count DESC ;

-- query 6: calculate the total revenue potential for each publisher (sum of prices of their games across platforms).
SELECT 
    c.name  as publisher_name,
    sum(vgp_platform.price)  as total_revenue_potential
FROM 
    video_game_publisher vgp
JOIN 
    contributor c ON vgp.dpid = c.dpid
JOIN 
    video_game_platforms vgp_platform ON vgp.vid = vgp_platform.vid
GROUP BY 
    c.name
ORDER BY 
    total_revenue_potential DESC ;
