-- AI can do a few things correctly

-- Inserting test user data without UID
INSERT INTO users (Username, Password, first_name, last_name, creation_date, last_access)
VALUES
  ('alice_wonder', 'passwordA1', 'Alice', 'Wonder', '2025-02-15', '2025-02-15 08:45:00'),
  ('bob_smith', 'passwordB2', 'Bob', 'Smith', '2025-01-20', '2025-01-20 09:30:00'),
  ('charlie_brown', 'passwordC3', 'Charlie', 'Brown', '2025-03-10', '2025-03-10 10:15:00'),
  ('david_lee', 'passwordD4', 'David', 'Lee', '2025-02-05', '2025-02-05 11:00:00'),
  ('emily_jones', 'passwordE5', 'Emily', 'Jones', '2025-03-18', '2025-03-18 13:00:00'),
  ('frank_white', 'passwordF6', 'Frank', 'White', '2025-01-12', '2025-01-12 14:25:00'),
  ('grace_black', 'passwordG7', 'Grace', 'Black', '2025-03-08', '2025-03-08 16:00:00'),
  ('hannah_grey', 'passwordH8', 'Hannah', 'Grey', '2025-02-28', '2025-02-28 17:30:00');

-- Inserting test email data without UID (assuming UID values are already known or will be assigned later)
INSERT INTO user_email (uid, email)
VALUES
  (1, 'alice.wonder@example.com'),
  (1, 'alice.wonder@workplace.com'),
  (2, 'bob.smith@example.com'),
  (3, 'charlie.brown@example.com'),
  (4, 'david.lee@example.com'),
  (5, 'emily.jones@example.com'),
  (6, 'frank.white@example.com'),
  (7, 'grace.black@example.com'),
  (8, 'hannah.grey@example.com');

-- Inserting test follow data without follower_uid and followee_uid
INSERT INTO follows (follower_uid, followee_uid)
VALUES
  (1, 2),  -- Alice follows Bob
  (1, 3),  -- Alice follows Charlie
  (2, 3),  -- Bob follows Charlie
  (3, 4),  -- Charlie follows David
  (4, 5),  -- David follows Emily
  (5, 6),  -- Emily follows Frank
  (6, 7),  -- Frank follows Grace
  (7, 8),  -- Grace follows Hannah
  (8, 1);  -- Hannah follows Alice

-- Inserting test platform data
INSERT INTO platform (name)
VALUES
  ('Xbox 360'),
  ('Xbox One'),
  ('Xbox Series S'),
  ('Xbox Series X'),
  ('Personal Computer'),
  ('Steam'),
  ('Epic Games'),
  ('Battlenet'),
  ('Nintendo 64'),
  ('Playstation'),
  ('Playstation 2'),
  ('Playstation 3'),
  ('Playstation 4'),
  ('Playstation 5');

-- Inserting test video game data
INSERT INTO video_games (esrb, title)
VALUES
  ('E', 'Super Mario Odyssey'),  -- Game rated "Everyone"
  ('T', 'Fortnite'),             -- Game rated "Teen"
  ('M', 'Grand Theft Auto V'),   -- Game rated "Mature"
  ('E10', 'Minecraft'),         -- Game rated "Everyone 10+"
  ('AO', 'Hot Coffee Mod');     -- Game rated "Adults Only" (fictitious example)

INSERT INTO genre (genre)
VALUES
  ('Action'),
  ('Adventure'),
  ('RPG'),
  ('Shooter'),
  ('Sports'),
  ('Simulation'),
  ('Strategy'),
  ('Fighting'),
  ('Horror'),
  ('Puzzle');

-- Inserting test video game genre data
INSERT INTO video_game_genre (vid, gid)
VALUES
  (1, 1),  -- 'Super Mario Odyssey' is an Action game (vid = 1, gid = 1)
  (2, 4),  -- 'Fortnite' is a Shooter game (vid = 2, gid = 4)
  (3, 7),  -- 'Grand Theft Auto V' is a Strategy game (vid = 3, gid = 7)
  (4, 1),  -- 'Minecraft' is an Action game (vid = 4, gid = 1)
  (5, 9);  -- 'Hot Coffee Mod' is a Puzzle game (vid = 5, gid = 9)

-- Inserting test contributor data
INSERT INTO contributor (name)
VALUES
  ('John Doe'),
  ('Jane Smith'),
  ('Chris Johnson'),
  ('Emily Davis'),
  ('Michael Brown');

-- Inserting test video game publisher data
INSERT INTO video_game_publisher (dpid, vid)
VALUES
  (1, 1),  -- John Doe publishes 'Super Mario Odyssey' (dpid = 1, vid = 1)
  (2, 2),  -- Jane Smith publishes 'Fortnite' (dpid = 2, vid = 2)
  (3, 3),  -- Chris Johnson publishes 'Grand Theft Auto V' (dpid = 3, vid = 3)
  (4, 4),  -- Emily Davis publishes 'Minecraft' (dpid = 4, vid = 4)
  (5, 5);  -- Michael Brown publishes 'Hot Coffee Mod' (dpid = 5, vid = 5)

-- Inserting test video game developer data
INSERT INTO video_game_developer (dpid, vid)
VALUES
  (1, 1),  -- John Doe developed 'Super Mario Odyssey' (dpid = 1, vid = 1)
  (2, 2),  -- Jane Smith developed 'Fortnite' (dpid = 2, vid = 2)
  (3, 3),  -- Chris Johnson developed 'Grand Theft Auto V' (dpid = 3, vid = 3)
  (4, 4),  -- Emily Davis developed 'Minecraft' (dpid = 4, vid = 4)
  (5, 5);  -- Michael Brown developed 'Hot Coffee Mod' (dpid = 5, vid = 5)

-- Inserting test video game platform data
INSERT INTO video_game_platforms (pid, vid, price, release_date)
VALUES
  (1, 1, 59.99, '2017-10-27'),  -- 'Super Mario Odyssey' on Twitter, released on Oct 27, 2017, priced at $59.99
  (2, 2, 0.00, '2017-09-26'),  -- 'Fortnite' on Facebook, released on Sep 26, 2017, free-to-play
  (3, 3, 39.99, '2013-09-17'),  -- 'Grand Theft Auto V' on Instagram, released on Sep 17, 2013, priced at $39.99
  (4, 4, 29.99, '2011-11-18'),  -- 'Minecraft' on LinkedIn, released on Nov 18, 2011, priced at $29.99
  (5, 5, 19.99, '2005-08-01');  -- 'Hot Coffee Mod' on TikTok, released on Aug 1, 2005, priced at $19.99

-- Inserting test user rating data
INSERT INTO user_rating (uid, vid, rating)
VALUES
  (1, 1, 5),  -- User 1 (Alice) rates 'Super Mario Odyssey' 5 stars
  (2, 2, 4),  -- User 2 (Bob) rates 'Fortnite' 4 stars
  (3, 3, 3),  -- User 3 (Charlie) rates 'Grand Theft Auto V' 3 stars
  (4, 4, 5),  -- User 4 (David) rates 'Minecraft' 5 stars
  (5, 5, 2);  -- User 5 (Emily) rates 'Hot Coffee Mod' 2 stars

-- Inserting test user play data
INSERT INTO user_plays (uid, vid, start_time, end_time)
VALUES
  (1, 1, '2025-03-20 08:00:00', '2025-03-20 10:00:00'),  -- Alice played 'Super Mario Odyssey' from 8 AM to 10 AM
  (2, 2, '2025-03-19 14:00:00', '2025-03-19 16:30:00'),  -- Bob played 'Fortnite' from 2 PM to 4:30 PM
  (3, 3, '2025-03-18 18:00:00', '2025-03-18 20:00:00'),  -- Charlie played 'Grand Theft Auto V' from 6 PM to 8 PM
  (4, 4, '2025-03-17 12:00:00', '2025-03-17 14:00:00'),  -- David played 'Minecraft' from 12 PM to 2 PM
  (5, 5, '2025-03-16 09:30:00', '2025-03-16 11:00:00');  -- Emily played 'Hot Coffee Mod' from 9:30 AM to 11 AM

-- Inserting test collection data
INSERT INTO collection (name)
VALUES
  ('Top Rated Games'),
  ('Action Adventures'),
  ('Multiplayer Madness'),
  ('Family Friendly'),
  ('Indie Gems');

-- Inserting test data for user collections
INSERT INTO user_has_collection (uid, cid)
VALUES
  (1, 1),  -- Alice is part of the 'Top Rated Games' collection (uid = 1, cid = 1)
  (2, 2),  -- Bob is part of the 'Action Adventures' collection (uid = 2, cid = 2)
  (3, 3),  -- Charlie is part of the 'Multiplayer Madness' collection (uid = 3, cid = 3)
  (4, 4),  -- David is part of the 'Family Friendly' collection (uid = 4, cid = 4)
  (5, 5);  -- Emily is part of the 'Indie Gems' collection (uid = 5, cid = 5)

-- Inserting test data for video games in collections
INSERT INTO collection_has_video_game (cid, vid)
VALUES
  (1, 1),  -- 'Super Mario Odyssey' is part of the 'Top Rated Games' collection (cid = 1, vid = 1)
  (2, 2),  -- 'Fortnite' is part of the 'Action Adventures' collection (cid = 2, vid = 2)
  (3, 3),  -- 'Grand Theft Auto V' is part of the 'Multiplayer Madness' collection (cid = 3, vid = 3)
  (4, 4),  -- 'Minecraft' is part of the 'Family Friendly' collection (cid = 4, vid = 4)
  (5, 5);  -- 'Hot Coffee Mod' is part of the 'Indie Gems' collection (cid = 5, vid = 5)

-- Inserting test data for user-platform associations
INSERT INTO user_platform (uid, pid)
VALUES
  (1, 1),  -- Alice uses Twitter (uid = 1, pid = 1)
  (2, 2),  -- Bob uses Facebook (uid = 2, pid = 2)
  (3, 3),  -- Charlie uses Instagram (uid = 3, pid = 3)
  (4, 4),  -- David uses LinkedIn (uid = 4, pid = 4)
  (5, 5);  -- Emily uses TikTok (uid = 5, pid = 5)
