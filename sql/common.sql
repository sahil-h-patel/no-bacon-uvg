-- User Data
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


-- Video Game Data

-- Contributor Data

-- Platform Data

-- Genre Data