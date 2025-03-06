create table users(
    uid int primary key,
    Username varchar(64) not null,
    Password varchar(64) not null,
    Firstname varchar(64),
    Lastname varchar(64),
    CreationDate date,
    LastAccess date
)

CREATE TABLE user_email(
    uid INT,
    email VARCHAR(64),
    PRIMARY KEY(uid, email),
    FOREIGN KEY(uid) REFERENCES users(uid)
)

CREATE TABLE follows(
    follower_uid INT,
    followee_uid INT,
    PRIMARY KEY (followee_uid, follower_uid),
    FOREIGN KEY(follower_uid) REFERENCES users(uid),
    FOREIGN KEY(followee_uid) REFERENCES users(uid)
)

CREATE TABLE platform(
    pid INT PRIMARY KEY,
    name VARCHAR(64) NOT NULL
)

CREATE TYPE ESRB_ratings AS ENUM('Everyone','Everyone 10+','Teen','Mature 17+','Rating Pending - Likely Mature 17+', 'Rating Pending', 'Adults Only 18+');
CREATE TABLE video_games(
    vid INT PRIMARY KEY,
    ESRB ESRB_ratings,
    Title VARCHAR(64) NOT NULL
);