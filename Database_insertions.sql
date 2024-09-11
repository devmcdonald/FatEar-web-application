INSERT INTO users (username, pwd, fname, lname, lastlogin, nickname) VALUES
 ('gwash', 'one', 'George', 'Washington', '2023-01-14', 'first'),
 ('jadams', 'two', 'John', 'Adams', '2022-07-04', 'second'), 
 ('tjeff', 'three', 'Thomas', 'Jefferson', '2022-07-04', 'third'),
 ('jmad', 'four', 'James', 'Madison', '2022-06-28', 'fourth'), 
 ('jmo', 'five', 'James', 'Monroe', '2022-07-04', 'fifth'),
 ('jqa', 'six', 'John', 'Quincy Adams', '2023-02-23', 'sixth'),
 ('ajack', 'seven', 'Andrew', 'Jackson', '2022-06-08', 'seventh'),
 ('mvb', 'eight', 'Martin', 'Van Buren', NULL, 'eighth'),
 ('whh', 'nine', 'William', 'Harrison', '2022-04-04', NULL),
 ('jtyler', NULL, 'John', 'Tyler', '2023-01-18', 'tenth');

INSERT INTO song (songID, title, releaseDate, songURL) VALUES
 ('00001', 'Flowers', '2023-01-01', 'flowers.com'),
 ('00002', 'Last Night', '2023-03-01', 'lastnight.com'), 
 ('00003', 'As It Was', '2023-02-01', 'asitwas.com'),
 ('00004', 'Die For You', '2022-12-15', 'dieforyou.com'),
 ('00005', 'Creepin', '2023-03-15', 'creepin.com'),
 ('00006', 'Boys a Liar', '2023-01-01', 'liar.com'),
 ('00007', 'Anti-Hero', '2022-08-15', 'antihero.com'),
 ('00008', 'Calm Down', '2022-09-15', 'calmdown.com'),
 ('00009', 'You Proof', '2022-11-01', NULL),
 ('00010', 'Jaded', NULL, 'jaded.com');

INSERT INTO artist (artistID, fname, lname, artistBio, artistURL) VALUES
 ('cyrus', 'Miley', 'Cyrus', 'Miley Ray Cyrus is an American singer, songwriter, and actress.', 'mileycyrus.com'),
 ('walle', 'Morgan', 'Wallen', 'Morgan Cole Wallen is an American country music singer and songwriter.', NULL),
 ('style', 'Harry', 'Styles', 'Harry Edward Styles is an English singer and songwriter.', 'harrystyles.com'), 
 ('grand', 'Ariana', 'Grande', 'Ariana Grande-Butera is an American singer, songwriter, and actress.', 'arianagrande.com'),
 ('boomi', 'Metro', 'Boomin', 'Leland Tyler Wayne, known professionally as Metro Boomin, is an American record producer and DJ.', 'metroboomin.com'),
 ('spice', 'Ice', 'Spice', NULL, NULL),
 ('swift', 'Taylor', 'Swift', 'Taylor Swift is an American singer-songwriter.', 'tswift.com'),
 ('gomez', 'Selena', 'Gomez', NULL, 'selenagomez.com');

INSERT INTO album (albumID) VALUES
 ('MC001'),
 ('MC002'),
 ('MW001'),
 ('HS001'),
 ('AG001'),
 ('MB001'),
 ('IC001'),
 ('TS001'),
 ('SG001');

INSERT INTO friend (user1, user2, acceptStatus, requestSentBy, createdAt, updatedAt) VALUES
 ('gwash', 'jadams', 'Accepted', 'jadams', '2022-01-01 11:00:00', '2022-02-15 01:00:00'),
 ('gwash', 'tjeff', NULL, 'gwash', '2022-04-01 16:00:00', '2023-02-01 18:00:00'),
 ('jadams', 'tjeff', 'Not Accepted', 'jadams', '2023-01-01 11:00:00', '2023-02-15 01:00:00'),
 ('tjeff', 'jmad', 'Accepted', 'tjeff', '2023-01-01 11:00:00', '2023-01-15 01:00:00'), 
 ('jmad', 'jmo', 'Pending', 'jmo', '2023-01-01 18:00:00', '2023-02-25 01:30:00'),
 ('gwash', 'jmo', 'Accepted', 'jmo', '2023-01-01 13:00:00', '2023-03-15 01:00:00'),
 ('jqa', 'tjeff', 'Accepted', 'jqa', NULL, '2021-02-15 01:00:00'),
 ('jqa', 'mvb', 'Not Accepted', 'jqa', '2022-08-01 11:00:00', '2023-01-15 08:00:00'),
 ('mvb', 'ajack', 'Accepted', NULL, '2019-09-10 19:00:00', '2020-11-15 01:00:00'),
 ('whh', 'jtyler', 'Not Accepted', 'whh', '2021-10-01 11:00:00', '2022-10-15 13:00:00'),
 ('whh', 'tjeff', 'Accepted', 'tjeff', '2020-12-01 11:00:00', '2021-04-15 01:00:00'),
 ('mvb', 'jadams', 'Pending', 'jadams', '2022-06-01 11:00:00', NULL),
 ('gwash', 'jmad', 'Pending', 'gwash', '2023-01-06 12:00:00', '2023-02-25 02:30:00');

INSERT INTO follows (follower, follows, createdAt) VALUES
 ('jqa', 'gwash', '2022-08-04 17:30:00'),
 ('mvb', 'tjeff', '2023-02-17 12:15:00'),
 ('whh', 'jmad', '2023-01-02 12:00:00'),
 ('jtyler', 'mvb', '2023-03-04 13:00:00'),
 ('ajack', 'jadams', '2023-01-01 01:12:00'), 
 ('tjeff', 'ajack', '2022-07-07 07:30:00'),
 ('jmo', 'jqa', '2022-02-03 12:12:12'),
 ('jmad', 'mvb', '2021-08-08 02:02:02'),
 ('jadams', 'jmo', NULL),
 ('gwash', 'jmad', NULL);

INSERT INTO rateAlbum (username, albumID, stars) VALUES
 ('gwash', 'MC001', 5),
 ('whh', 'MC001', 5),
 ('jqa', 'MC001', 3),
 ('gwash', 'MC002', 4),
 ('ajack', 'MC002', 5),
 ('mvb', 'MC002', 4),
 ('jadams', 'MW001', 5),
 ('jtyler', 'MW001', 2),
 ('jmo', 'MW001', 3),
 ('whh', 'HS001', 4),
 ('jmad', 'HS001', 1),
 ('mvb', 'HS001', NULL),
 ('tjeff', 'AG001', 3),
 ('jtyler', 'AG001', 5),
 ('jqa', 'AG001', 4),
 ('tjeff', 'MB001', 4),
 ('jadams', 'MB001', 5),
 ('gwash', 'MB001', 5),
 ('ajack', 'IC001', 3),
 ('jmo', 'IC001', 4),
 ('jmad', 'IC001', 4),
 ('mvb','TS001', 5),
 ('gwash', 'TS001', 5),
 ('jmad', 'TS001', 3),
 ('whh', 'SG001', 1),
 ('jadams', 'SG001', 3),
 ('ajack', 'SG001', 4);
  
  
  
  INSERT INTO reviewAlbum (username, albumID, reviewText, reviewDate) VALUES
  ('jadams', 'MC001', 'Best album ever', '2023-02-23'),
  ('tjeff', 'MC002', 'Decent listen', '2022-05-05'),
  ('jqa', 'MC002', NULL, NULL),
  ('gwash', 'MW001', 'Terrible', '2023-02-27'),
  ('jmo', 'HS001', 'Not bad', '2022-09-14'),
  ('whh', 'AG001', 'Worst album ever', '2022-11-23'),
  ('jmad', 'AG001', NULL, '2022-10-26'),
  ('mvb', 'MB001', 'Relaxing album', '2022-12-30'),
  ('ajack', 'IC001', 'Not worth the listen', '2022-06-24'),
  ('jmad', 'TS001', 'Great vibes', '2023-02-14'),
  ('jtyler', 'TS001', 'Loved', NULL),
  ('jtyler', 'SG001', 'Did not enjoy', '2023-03-29');

-- Insert into rateSong
INSERT INTO rateSong (username, songID, stars, ratingDate) VALUES
  ('gwash', '00001', 4, '2022-04-16'),
  ('jmad', '00001', 5, '2022-08-10'),
  ('tjeff', '00001', 4, '2022-10-16'),
  ('mvb', '00002', 4, '2022-06-13'),
  ('whh', '00002', 5, '2022-01-14'),
  ('ajack', '00002', 2, '2022-01-12'),
  ('jadams', '00003', 4, '2022-11-03'),
  ('jmo', '00003', 5, '2021-07-06'),
  ('tjeff', '00003', 5, '2022-11-03'),
  ('jqa', '00004', 1, '2022-04-12'),
  ('jtyler', '00004', 2, '2022-06-05'),
  ('ajack', '00004', 3, '2022-09-08'),
  ('whh', '00005', 4, '2022-07-12'),
  ('gwash', '00005', 5, '2022-08-15'),
  ('tjeff', '00005', 2, '2022-09-09'),
  ('jadams', '00006', 5, '2022-01-19'),
  ('mvb', '00006', 5, '2022-12-05'),
  ('jmo', '00006', 5, '2022-12-08'),
  ('jmad', '00007', 5, '2022-08-04'),
  ('jtyler', '00007', 2, '2022-10-19'),
  ('whh', '00007', 3, '2022-02-14'),
  ('gwash', '00008', 5, '2022-03-25'),
  ('whh', '00008', 3, '2022-06-05'),
  ('jqa', '00008', 5, NULL),
  ('ajack', '00009', 5, '2022-09-18'),
  ('jqa', '00009', NULL, '2022-02-13'),
  ('jmo', '00009', NULL, NULL),
  ('whh', '00010', 4, '2022-03-13'),
  ('gwash', '00010', 5, '2022-04-19'),
  ('jtyler', '00010', 5, '2022-06-22');

-- Insert into reviewSong
INSERT INTO reviewSong (username, songID, reviewText, reviewDate) VALUES
  ('gwash', '00001', 'Great song!', '2022-04-16'),
  ('jqa', '00001', 'Loved', '2022-08-10'),
  ('mvb', '00002', 'Could be better', '2022-01-13'),
  ('whh', '00002', 'Amazing', '2022-01-14'),
  ('jmo', '00003', 'The best', '2021-07-06'),
  ('ajack', '00003', 'Not my favorite', '2022-08-08'),
  ('jqa', '00004', 'Worst song ever', NULL),
  ('jmo', '00004', 'Okay', '2022-09-08'),
  ('jqa', '00005', 'Favorite song', '2021-08-15'),
  ('jtyler', '00005', 'Terrible', '2022-11-09'),
  ('jmad', '00006', 'Great!', '2022-01-19'),
  ('mvb', '00006', 'The best!', '2022-12-05'),
  ('tjeff', '00007', 'Not the best', '2022-09-19'),
  ('jmad', '00007', 'Satisfactory', '2022-06-17'),
  ('mvb', '00008', 'Above Average', '2022-06-25'),
  ('jqa', '00008', 'Amazing', NULL),
  ('jtyler', '00009', NULL, '2022-07-28'),
  ('ajack', '00009', NULL, NULL),
  ('gwash', '00010', 'Fantastic', '2022-04-19'),
  ('jtyler', '00010', 'Amazing', '2022-08-22');

-- Insert into songInAlbum
INSERT INTO songInAlbum (albumID, songID) VALUES
  ('MC001', '00001'),
  ('MC002', '00010'),
  ('MW001', '00002'),
  ('MW001', '00009'),
  ('HS001', '00003'),
  ('AG001', '00004'),
  ('MB001', '00005'),
  ('IC001', '00006'),
  ('TS001', '00007'),
  ('SG001', '00008');

-- Insert into songGenre
INSERT INTO songGenre (songID, genre) VALUES
  ('00001', 'Pop'),
  ('00002', 'Country'),
  ('00003', 'Pop'),
  ('00004', 'R&B'),
  ('00005', 'Rap'),
  ('00006', 'Pop'),
  ('00007', 'Pop'),
  ('00008', 'Pop'),
  ('00009', 'Country'),
  ('00010', 'Pop');

-- Insert into artistPerformsSong
INSERT INTO artistPerformsSong (artistID, songID) VALUES
  ('cyrus', '00001'),
  ('cyrus', '00010'),
  ('walle', '00002'),
  ('style', '00003'),
  ('grand', '00004'),
  ('boomi', '00005'),
  ('spice', '00006'),
  ('swift', '00007'),
  ('gomez', '00008'),
  ('walle', '00009');

-- Insert into userFanOfArtist
INSERT INTO userFanOfArtist (username, artistID) VALUES
  ('gwash', 'cyrus'),
  ('gwash', 'gomez'),
  ('gwash', 'grand'),
  ('jadams', 'walle'),
  ('tjeff', 'spice'),
  ('tjeff', 'swift'),
  ('jmad', 'grand'),
  ('jmo', 'style'),
  ('jmo', 'swift'),
  ('jqa', 'boomi'),
  ('jqa', 'gomez'),
  ('jqa', 'spice'),
  ('ajack', 'swift'),
  ('ajack', 'walle'),
  ('mvb', 'cyrus'),
  ('whh', 'cyrus'),
  ('whh', 'style'),
  ('whh', 'grand'),
  ('jtyler', 'gomez');
  
  
  
  
  