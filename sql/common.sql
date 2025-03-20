-- User Data
    -- Login queries
        -- Validate username and password
SELECT 
    uid, Username, Password 
FROM 
    users
WHERE 
    Username = '' -- Replace with the entered username
    AND Password = ''; -- Replace with the entered password
        -- Update last access 
UPDATE 
    users
SET 
    LastAccess = CURRENT_TIMESTAMP
WHERE 
    uid = ''; -- Replace with the user's unique ID (retrieved from the first query)
        -- 

    -- get all users specific user follows
select Username from users where uid in (
    select follows.followee_uid from follows where follower_uid=*****INSERT-ID HERE******
    );
    -- Get number of people specific user follows
select COUNT(Username) from users where uid in (
    select follows.followee_uid from follows where follower_uid=*****INSERT-ID HERE******
    )
    -- get all users that follow specific user
select Username from users where uid in (
    select follows.follower_uid from follows where follower_uid=*****INSERT-ID HERE******
    );
    -- Get number of people specific user follows
select COUNT(Username) from users where uid in (
    select follows.follower_uid from follows where follower_uid=*****INSERT-ID HERE******
    ) 

    -- Rating a Video Game
INSERT INTO user_rating (uid, vid, rating)
    VALUES ('', '', ''); -- Replace the placeholders with the user's ID, video game's ID, and the rating (1 to 5).
 
-- Get data about collection as per the document
    SELECT 
    c.name AS Collection_Name,
    COUNT(chvg.vid) AS Number_of_Video_Games,
    COALESCE(SUM(EXTRACT(EPOCH FROM (up.end_time - up.start)) / 3600), 0) AS Total_Playtime_Hours
FROM 
    collection c
LEFT JOIN 
    user_has_collection uhc ON c.cid = uhc.cid
LEFT JOIN 
    collection_has_video_game chvg ON c.cid = chvg.cid
LEFT JOIN 
    user_plays up ON chvg.vid = up.vid AND uhc.uid = up.uid
WHERE 
    uhc.uid = '' -- Replace with the user's ID
GROUP BY 
    c.name
ORDER BY 
    c.name ASC;

-- Video Game Data

-- Contributor Data

-- Platform Data

-- Genre Data

-- Collection Data
    -- Add Video game to user's collection 
    -- where first 2 queries are for checking that the collection is valid and it is the user's collection

SELECT * FROM collection WHERE cid = ''; -- Replace '' with the collection ID.
SELECT * FROM user_has_collection WHERE uid = '' AND cid = ''; -- Replace with user ID and collection ID.
INSERT INTO user_has_collection (uid, cid)
VALUES ('', ''); -- Replace '' with the user's ID and the collection's ID.
INSERT INTO collection_has_video_game (cid, vid)
VALUES ('', ''); -- Replace '' with the collection's ID and the video game's ID.


-- Searching for user based on email
SELECT 
    u.uid AS User_ID,
    u.Username,
    u.Firstname,
    u.Lastname,
    u.CreationDate,
    u.LastAccess,
    ue.email AS Email
FROM 
    users u
JOIN 
    user_email ue ON u.uid = ue.uid
WHERE 
    ue.email = 'user_email@example.com'; -- Replace 'user_email@example.com' with the desired email


-- Searching for Video Game data -- this was Copilot, damn good for this ngl

SELECT
    vg.Title AS Video_Game_Name,
    p.name AS Platform_Name,
    d.name AS Developer_Name,
    pub.name AS Publisher_Name,
    vg_platform.price AS Price,
    vg_platform.release_date AS Release_Date,
    vg.ESRB AS Age_Rating,
    ur.rating AS User_Rating,
    AVG(EXTRACT(EPOCH FROM (up.end_time - up.start)) / 3600) AS Average_Playtime_Hours
FROM
    video_games vg
JOIN
    video_game_platforms vg_platform ON vg.vid = vg_platform.vid
JOIN
    platform p ON vg_platform.pid = p.pid
LEFT JOIN
    video_game_developer vg_dev ON vg.vid = vg_dev.vid
LEFT JOIN
    contributor d ON vg_dev.dpid = d.dpid
LEFT JOIN
    video_game_publisher vg_pub ON vg.vid = vg_pub.vid
LEFT JOIN
    contributor pub ON vg_pub.dpid = pub.dpid
LEFT JOIN
    user_plays up ON vg.vid = up.vid
LEFT JOIN
    user_rating ur ON vg.vid = ur.vid
LEFT JOIN
    video_game_genre vg_genre ON vg.vid = vg_genre.vid
LEFT JOIN
    genre g ON vg_genre.gid = g.gid
WHERE
    vg.Title ILIKE '%game_name%' -- Replace 'game_name' with the desired title or partial title
    AND p.name ILIKE '%platform_name%' -- Replace 'platform_name' with the desired platform
    AND vg_platform.release_date >= 'start_date' -- Replace with the start date
    AND vg_platform.release_date <= 'end_date' -- Replace with the end date
    AND d.name ILIKE '%developer_name%' -- Replace 'developer_name' with the desired developer
    AND pub.name ILIKE '%publisher_name%' -- Replace 'publisher_name' with the desired publisher
    AND vg_platform.price <= '%desired_price%' -- Replace 'desired_price' with the price ceiling
    AND g.genre ILIKE '%genre_name%' -- Replace 'genre_name' with the desired genre
GROUP BY
    vg.Title, p.name, d.name, pub.name, vg_platform.price, vg_platform.release_date, vg.ESRB, ur.rating;
