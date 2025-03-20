-----------------------------------------------------------------
--------------------- User stats --------------------------------
-----------------------------------------------------------------

-- Query 1: Count the total number of collections owned by each user.
SELECT 
    u.Username AS User_Name,
    COUNT(uhc.cid) AS Total_Collections
FROM 
    users u
LEFT JOIN 
    user_has_collection uhc ON u.uid = uhc.uid
GROUP BY 
    u.Username
ORDER BY 
    Total_Collections DESC;

-- Query 2: Count the total number of video games in collections owned by each user.
SELECT 
    u.Username AS User_Name,
    COUNT(chvg.vid) AS Total_Video_Games_In_Collections
FROM 
    users u
LEFT JOIN 
    user_has_collection uhc ON u.uid = uhc.uid
LEFT JOIN 
    collection_has_video_game chvg ON uhc.cid = chvg.cid
GROUP BY 
    u.Username
ORDER BY 
    Total_Video_Games_In_Collections DESC;

-- Query 3: Calculate the average number of video games per collection for each user.
SELECT 
    u.Username AS User_Name,
    AVG(Collection_Video_Games.Total_Games) AS Avg_Games_Per_Collection
FROM 
    users u
LEFT JOIN 
    user_has_collection uhc ON u.uid = uhc.uid
LEFT JOIN (
    SELECT 
        chvg.cid,
        COUNT(chvg.vid) AS Total_Games
    FROM 
        collection_has_video_game chvg
    GROUP BY 
        chvg.cid
) AS Collection_Video_Games ON uhc.cid = Collection_Video_Games.cid
GROUP BY 
    u.Username
ORDER BY 
    Avg_Games_Per_Collection DESC;

-- Query 4: Calculate the total playtime (in hours) for all video games in collections owned by each user.
SELECT 
    u.Username AS User_Name,
    COALESCE(SUM(EXTRACT(EPOCH FROM (up.end_time - up.start)) / 3600), 0) AS Total_Playtime_Hours
FROM 
    users u
LEFT JOIN 
    user_has_collection uhc ON u.uid = uhc.uid
LEFT JOIN 
    collection_has_video_game chvg ON uhc.cid = chvg.cid
LEFT JOIN 
    user_plays up ON chvg.vid = up.vid AND up.uid = u.uid
GROUP BY 
    u.Username
ORDER BY 
    Total_Playtime_Hours DESC;

-- Query 5: Find the collection with the most video games for each user.
SELECT 
    u.Username AS User_Name,
    c.name AS Collection_Name,
    COUNT(chvg.vid) AS Total_Video_Games
FROM 
    users u
LEFT JOIN 
    user_has_collection uhc ON u.uid = uhc.uid
LEFT JOIN 
    collection c ON uhc.cid = c.cid
LEFT JOIN 
    collection_has_video_game chvg ON c.cid = chvg.cid
GROUP BY 
    u.Username, c.name
ORDER BY 
    u.Username, Total_Video_Games DESC;

-----------------------------------------------------------------
--------------------- Video Game stats --------------------------
-----------------------------------------------------------------

-- Query 1: Count the total number of video games in the database.
SELECT 
    COUNT(*) AS Total_Video_Games
FROM 
    video_games;

-- Query 2: Calculate the total price of video games grouped by platform.
SELECT 
    p.name AS Platform_Name,
    SUM(vg_platform.price) AS Total_Price_of_Video_Games
FROM 
    video_game_platforms vg_platform
JOIN 
    platform p ON vg_platform.pid = p.pid
GROUP BY 
    p.name
ORDER BY 
    Total_Price_of_Video_Games DESC;

-- Query 3: Count the number of video games for each genre.
SELECT 
    g.genre AS Genre_Name,
    COUNT(vg_genre.vid) AS Video_Game_Count
FROM 
    video_game_genre vg_genre
JOIN 
    genre g ON vg_genre.gid = g.gid
GROUP BY 
    g.genre
ORDER BY 
    Video_Game_Count DESC;

-- Query 4: Calculate the total playtime (in hours) of video games for each user.
SELECT 
    u.Username AS User_Name,
    COALESCE(SUM(EXTRACT(EPOCH FROM (up.end_time - up.start)) / 3600), 0) AS Total_Playtime_Hours
FROM 
    users u
LEFT JOIN 
    user_plays up ON u.uid = up.uid
GROUP BY 
    u.Username
ORDER BY 
    Total_Playtime_Hours DESC;

-- Query 5: Count the number of video games each user has rated.
SELECT 
    u.Username AS User_Name,
    COUNT(ur.vid) AS Rated_Video_Games
FROM 
    users u
LEFT JOIN 
    user_rating ur ON u.uid = ur.uid
GROUP BY 
    u.Username
ORDER BY 
    Rated_Video_Games DESC;

-----------------------------------------------------------------
--------------------- Publisher/Developer stats -----------------
-----------------------------------------------------------------

-- Query 1: Count the total number of video games published by each publisher.
SELECT 
    c.name AS Publisher_Name,
    COUNT(vgp.vid) AS Total_Video_Games_Published
FROM 
    video_game_publisher vgp
JOIN 
    contributor c ON vgp.dpid = c.dpid
GROUP BY 
    c.name
ORDER BY 
    Total_Video_Games_Published DESC;

-- Query 2: Count the total number of video games developed by each developer.
SELECT 
    c.name AS Developer_Name,
    COUNT(vgd.vid) AS Total_Video_Games_Developed
FROM 
    video_game_developer vgd
JOIN 
    contributor c ON vgd.dpid = c.dpid
GROUP BY 
    c.name
ORDER BY 
    Total_Video_Games_Developed DESC;

-- Query 3: Find publishers who have also developed video games, along with counts for publishing and developing.
SELECT 
    c.name AS Contributor_Name,
    COUNT(DISTINCT vgp.vid) AS Total_Published,
    COUNT(DISTINCT vgd.vid) AS Total_Developed
FROM 
    contributor c
LEFT JOIN 
    video_game_publisher vgp ON c.dpid = vgp.dpid
LEFT JOIN 
    video_game_developer vgd ON c.dpid = vgd.dpid
GROUP BY 
    c.name
ORDER BY 
    Total_Published DESC, Total_Developed DESC;

-- Query 4: Calculate the average number of video games published by publishers.
SELECT 
    AVG(Published_Games.Total_Published) AS Average_Games_Published
FROM (
    SELECT 
        c.name AS Publisher_Name,
        COUNT(vgp.vid) AS Total_Published
    FROM 
        video_game_publisher vgp
    JOIN 
        contributor c ON vgp.dpid = c.dpid
    GROUP BY 
        c.name
) AS Published_Games;

-- Query 5: Find the most common ESRB rating for games published by each publisher.
SELECT 
    c.name AS Publisher_Name,
    vg.ESRB AS Most_Common_ESRB_Rating,
    COUNT(vg.vid) AS Game_Count
FROM 
    video_game_publisher vgp
JOIN 
    contributor c ON vgp.dpid = c.dpid
JOIN 
    video_games vg ON vgp.vid = vg.vid
GROUP BY 
    c.name, vg.ESRB
ORDER BY 
    c.name, Game_Count DESC;

-- Query 6: Calculate the total revenue potential for each publisher (sum of prices of their games across platforms).
SELECT 
    c.name AS Publisher_Name,
    SUM(vgp_platform.price) AS Total_Revenue_Potential
FROM 
    video_game_publisher vgp
JOIN 
    contributor c ON vgp.dpid = c.dpid
JOIN 
    video_game_platforms vgp_platform ON vgp.vid = vgp_platform.vid
GROUP BY 
    c.name
ORDER BY 
    Total_Revenue_Potential DESC;
