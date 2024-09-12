create table users (
    username varchar(20) not null,
    pwd text,
    fname varchar(20) not null,
    lname varchar(20) not null,
    lastlogin date, 
    nickname varchar(20),
    primary key (username)
);

create table song (
    songID varchar(5),
    title varchar(20) not null,
    releaseDate date,
    songURL varchar(50),
    primary key (songID)
);

create table artist (
    artistID varchar(5),
    fname varchar(20) not null,
    lname varchar(20) not null,
    artistBio varchar(100),
    artistURL varchar(50),
    primary key (artistID)
);

create table album (
    albumID varchar(5),
    title text,
    primary key (albumID)
);

create table friend (
    user1 varchar(20),
    user2 varchar(20),
    acceptStatus varchar(20) check (acceptStatus in ('Accepted', 'Not Accepted', 'Pending')),
    requestSentBy varchar(20),
    createdAt timestamp,
    updatedAt timestamp,
    primary key (user1, user2),
    foreign key (user1) references users(username) on delete cascade,
    foreign key (user2) references users(username) on delete cascade
);

create table follows (
    follower varchar(20),
    follows varchar(20),
    createdAt timestamp,
    primary key (follower, follows),
    foreign key (follower) references users(username) on delete cascade,
    foreign key (follows) references users(username) on delete cascade
);

create table rateAlbum (
    username varchar(20),
    albumID varchar(5),
    stars int check (stars in (1,2,3,4,5)),
    primary key (username, albumID),
    foreign key (username) references users(username) on delete cascade,
    foreign key (albumID) references album(albumID) on delete cascade
);

create table reviewAlbum (
    username varchar(20),
    albumID varchar(5),
    reviewText varchar(100),
    reviewDate date,
    primary key (username, albumID),
    foreign key (username) references users(username) on delete cascade,
    foreign key (albumID) references album(albumID) on delete cascade
);

create table rateSong (
    username varchar(20),
    songID varchar(5),
    stars int check (stars in (1,2,3,4,5)),
    ratingDate date, 
    primary key (username, songID),
    foreign key (username) references users(username) on delete cascade,
    foreign key (songID) references song(songID) on delete cascade
);

create table reviewSong (
    username varchar(20),
    songID varchar(5),
    reviewText varchar(100),
    reviewDate date,
    primary key (username, songID),
    foreign key (username) references users(username) on delete cascade,
    foreign key (songID) references song(songID) on delete cascade
);

create table songInAlbum (
    albumID varchar(5),
    songID varchar(5),
    primary key (albumID, songID),
    foreign key (albumID) references album(albumID) on delete cascade,
    foreign key (songID) references song(songID) on delete cascade
);

create table songGenre (
    songID varchar(5),
    genre varchar(10),
    primary key (songID, genre),
    foreign key (songID) references song(songID) on delete cascade
);

create table artistPerformsSong (
    artistID varchar(5),
    songID varchar(5),
    primary key (artistID, songID),
    foreign key (artistID) references artist(artistID) on delete cascade,
    foreign key (songID) references song(songID) on delete cascade
);

create table userFanOfArtist (
    username varchar(20),
    artistID varchar(5),
    primary key (username, artistID),
    foreign key (username) references users(username) on delete cascade,
    foreign key (artistID) references artist(artistID) on delete cascade
);