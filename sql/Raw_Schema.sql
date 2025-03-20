-- Raw meaning there is no test data

CREATE TABLE users(
    uid SERIAL PRIMARY KEY,
    username VARCHAR(64) not null unique,
    password VARCHAR(64) not null,
    first_name VARCHAR(64),
    last_name VARCHAR(64),
    creation_date date,
    last_access timestamp
);

CREATE TABLE user_email(
    uid SERIAL,
    email VARCHAR(64),
    PRIMARY KEY(uid, email),
    FOREIGN KEY(uid) REFERENCES users(uid)
);

CREATE TABLE follows(
    follower_uid SERIAL,
    followee_uid SERIAL,
    PRIMARY KEY (followee_uid, follower_uid),
    FOREIGN KEY(follower_uid) REFERENCES users(uid),
    FOREIGN KEY(followee_uid) REFERENCES users(uid)
);

CREATE TABLE platform(
    pid SERIAL PRIMARY KEY,
    name VARCHAR(64) NOT NULL
);

CREATE TYPE esrb_ratings AS ENUM('RP', 'RPM', 'E', 'E10', 'T', 'M', 'AO');
CREATE TABLE video_games(
    vid SERIAL PRIMARY KEY,
    esrb esrb_ratings,
    title VARCHAR(64) NOT NULL
);

CREATE TABLE genre(
    gid SERIAL PRIMARY KEY,
    genre VARCHAR(64)
);

CREATE TABLE video_game_genre(
    vid SERIAL,
    gid SERIAL,
    primary key(vid, gid),
    FOREIGN KEY(vid) REFERENCES video_games(vid),
    FOREIGN KEY(gid) REFERENCES genre(gid)
);

CREATE TABLE contributor(
    dpid SERIAL PRIMARY KEY ,
    name varchar(64)
);

CREATE TABLE video_game_publisher(
    dpid SERIAL,
    vid SERIAL,
    PRIMARY KEY (dpid, vid),
    FOREIGN KEY (dpid) REFERENCES contributor(dpid),
    FOREIGN KEY (vid) REFERENCES video_games(vid)
);

CREATE TABLE video_game_developer(
    dpid SERIAL,
    vid SERIAL,
    PRIMARY KEY (dpid, vid),
    FOREIGN KEY (dpid) REFERENCES contributor(dpid),
    FOREIGN KEY (vid) REFERENCES video_games(vid)
);

CREATE TABLE video_game_platforms(
    pid SERIAL,
    vid SERIAL,
    price decimal(4,2),
    release_date date,
    PRIMARY KEY (pid, vid),
    FOREIGN KEY (pid) REFERENCES platform(pid),
    FOREIGN KEY (vid) REFERENCES video_games(vid)

);

CREATE TYPE rating_scale AS ENUM('1','2','3','4','5');
CREATE TABLE user_rating(
    uid SERIAL,
    vid SERIAL,
    rating rating_scale,
    PRIMARY KEY (uid, vid, rating),
    FOREIGN KEY (uid) REFERENCES users(uid),
    FOREIGN KEY (vid) REFERENCES video_games(vid)
);

CREATE TABLE user_plays(
    uid SERIAL,
    vid SERIAL,
    start timestamp,
    end_time timestamp, -- end is a keyword and would be quoted but I didn't want to have that mess up queries so I changed the name
    PRIMARY KEY (uid, vid, start),
    FOREIGN KEY (uid) REFERENCES users(uid),
    FOREIGN KEY (vid) REFERENCES video_games(vid)

);

CREATE TABLE collection(
    cid SERIAL PRIMARY KEY ,
    name VARCHAR(64)
);

CREATE TABLE user_has_collection(
    uid SERIAL,
    cid SERIAL,
    PRIMARY KEY (uid, cid),
    FOREIGN KEY (uid) REFERENCES users(uid),
    FOREIGN KEY (cid) REFERENCES collection(cid)
);

CREATE TABLE collection_has_video_game(
    cid SERIAL,
    vid SERIAL,
    PRIMARY KEY (cid, vid),
    FOREIGN KEY (cid) REFERENCES collection(cid),
    FOREIGN KEY (vid) REFERENCES video_games(vid)
);

CREATE TABLE user_platform(
    uid SERIAL, 
    pid SERIAL, 
    PRIMARY KEY (uid,pid),
    FOREIGN KEY(uid) REFERENCES users(uid),
    FOREIGN KEY(pid) REFERENCES platform(pid)
);
