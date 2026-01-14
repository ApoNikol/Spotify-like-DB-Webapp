-- USER table
CREATE TABLE APP_USER (
    username VARCHAR(255),
    email VARCHAR(255) UNIQUE,
    Birthday DATE,
    PRIMARY KEY (username)
);

-- SONG table
CREATE TABLE Song (
    song_id SERIAL PRIMARY KEY,
    song_name VARCHAR(255),
    artist VARCHAR(255),
    duration TIME,
    ReleaseDate DATE,
    FOREIGN KEY (artist) REFERENCES APP_USER(username)
);

-- ALBUM table
CREATE TABLE Album (
    album_id SERIAL PRIMARY KEY, 
    title VARCHAR(255),
    artist VARCHAR(255),
    ReleaseDate DATE,
    FOREIGN KEY (artist) REFERENCES APP_USER(username)
);

-- Podcast table
CREATE TABLE Podcast (
    title VARCHAR(255), 
    creator VARCHAR(255),
    duration TIME,
    ReleaseDate DATE,
    PRIMARY KEY (title, creator),
    FOREIGN KEY (creator) REFERENCES APP_USER(username)
);

-- PLAYLIST table
CREATE TABLE Playlist (
    playlist_id SERIAL, 
    user_name VARCHAR(255),
    name VARCHAR(255),
    PRIMARY KEY (playlist_id, user_name),
    FOREIGN KEY (user_name) REFERENCES APP_USER(username)
);

--SONGLIST table
CREATE TABLE songlist(
song_id INT,
playlist_id INT,
user_id VARCHAR(255),
PRIMARY KEY (user_id, playlist_id, song_id),
FOREIGN KEY (song_id) REFERENCES Song(song_id),
FOREIGN KEY (playlist_id, user_id) REFERENCES Playlist(playlist_id, user_name),
FOREIGN KEY (user_id) REFERENCES APP_USER(username)
);

-- COMPONENTS table
CREATE TABLE Components (
    album_id INT,
    song_id INT,
user_id VARCHAR(255),
    song_order INT,
    PRIMARY KEY (album_id, song_id, user_id),
FOREIGN KEY (user_id) REFERENCES APP_USER(username),
    FOREIGN KEY (album_id) REFERENCES Album(album_id),
    FOREIGN KEY (song_id) REFERENCES Song(song_id)
);

-- FEATURES table
CREATE TABLE Features (
    song_id INT,
    artist VARCHAR(255),
    PRIMARY KEY (song_id, artist),
    FOREIGN KEY (song_id) REFERENCES Song(song_id),
    FOREIGN KEY (artist) REFERENCES APP_USER(username)
);


CREATE INDEX idx_song_artist ON Song(artist);
CREATE INDEX idx_album_artist ON Album(artist);
CREATE INDEX idx_components_album ON Components(album_id);