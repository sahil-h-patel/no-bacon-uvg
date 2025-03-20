-- User Data
    -- get all users specific user follows
select Username, COUNT(Username) from users where uid in (
    select follows.followee_uid from follows where follower_uid=*****INSERT-ID HERE******
    ) 
    group by Username;

-- Video Game Data

-- Contributor Data

-- Platform Data

-- Genre Data

    -- Average Rating based on Genre
    -- SELECT (v.title, v.ESRB, g.genre) from video_games as v left join 