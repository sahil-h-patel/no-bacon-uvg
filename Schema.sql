CREATE TABLE users(
    uid INT PRIMARY KEY,
    Username VARCHAR(64) not null,
    Password VARCHAR(64) not null,
    Firstname VARCHAR(64),
    Lastname VARCHAR(64),
    CreationDate date,
    LastAccess date
);

CREATE TABLE user_email(
    uid INT,
    email VARCHAR(64),
    PRIMARY KEY(uid, email),
    FOREIGN KEY(uid) REFERENCES users(uid)
);

CREATE TABLE follows(
    follower_uid INT,
    followee_uid INT,
    PRIMARY KEY (followee_uid, follower_uid),
    FOREIGN KEY(follower_uid) REFERENCES users(uid),
    FOREIGN KEY(followee_uid) REFERENCES users(uid)
);

CREATE TABLE platform(
    pid INT PRIMARY KEY,
    name VARCHAR(64) NOT NULL
);

CREATE TYPE ESRB_ratings AS ENUM('Everyone','Everyone 10+','Teen','Mature 17+','Rating Pending - Likely Mature 17+', 'Rating Pending', 'Adults Only 18+');
CREATE TABLE video_games(
    vid INT PRIMARY KEY,
    ESRB ESRB_ratings,
    Title VARCHAR(64) NOT NULL
);

CREATE TABLE genre(
    gid INT PRIMARY KEY,
    genre VARCHAR(64)
);

CREATE TABLE video_game_genre(
    vid int,
    gid int,
    primary key(vid, gid),
    FOREIGN KEY(vid) REFERENCES video_games(vid),
    FOREIGN KEY(gid) REFERENCES genre(gid)
);

CREATE TABLE contributor(
    dpid int primary key,
    name varchar(64)
);

CREATE TABLE video_game_publisher(
    dpid INT,
    vid INT,
    PRIMARY KEY (dpid, vid),
    FOREIGN KEY (dpid) REFERENCES contributor(dpid),
    FOREIGN KEY (vid) REFERENCES video_games(vid)
);
CREATE TABLE video_game_developer(
    dpid INT,
    vid INT,
    PRIMARY KEY (dpid, vid),
    FOREIGN KEY (dpid) REFERENCES contributor(dpid),
    FOREIGN KEY (vid) REFERENCES video_games(vid)
);

CREATE TABLE video_game_platforms(
    pid INT,
    vid INT,
    price decimal(4,2),
    release_date date,
    PRIMARY KEY (pid, vid),
    FOREIGN KEY (pid) REFERENCES platform(pid),
    FOREIGN KEY (vid) REFERENCES video_games(vid)

);

CREATE TYPE rating_scale AS ENUM('1','2','3','4','5');
CREATE TABLE user_rating(
    uid INT,
    vid INT,
    rating rating_scale,
    PRIMARY KEY (uid, vid, rating),
    FOREIGN KEY (uid) REFERENCES users(uid),
    FOREIGN KEY (vid) REFERENCES video_games(vid)
);

CREATE TABLE user_plays(
    uid INT,
    vid INT,
    start timestamp,
    end_time timestamp, -- end is a keyword and would be quoted but I didn't want to have that mess up queries so I changed the name
    PRIMARY KEY (uid, vid, start),
    FOREIGN KEY (uid) REFERENCES users(uid),
    FOREIGN KEY (vid) REFERENCES video_games(vid)

);

CREATE TABLE collection(
    cid int PRIMARY KEY,
    name VARCHAR(64)
);

CREATE TABLE user_has_collection(
    uid INT,
    cid INT,
    PRIMARY KEY (uid, cid),
    FOREIGN KEY (uid) REFERENCES users(uid),
    FOREIGN KEY (cid) REFERENCES collection(cid)
);

CREATE TABLE collection_has_video_game(
    cid INT,
    vid INT,
    PRIMARY KEY (cid, vid),
    FOREIGN KEY (cid) REFERENCES collection(cid),
    FOREIGN KEY (vid) REFERENCES video_games(vid)
);
