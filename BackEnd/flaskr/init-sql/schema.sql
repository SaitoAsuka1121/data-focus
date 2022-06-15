DROP TABLE IF EXISTS user;
DROP TABLE IF EXISTS databases;
DROP TABLE IF EXISTS tables;
CREATE TABLE user (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  username TEXT UNIQUE NOT NULL,
  password TEXT NOT NULL
);
CREATE TABLE databases (
    display_name TEXT UNIQUE PRIMARY KEY NOT NULL,
    sqlalchemy_uri TEXT NOT NULL,
    owner TEXT NOT NULL
);
CREATE TABLE tables (
    display_name TEXT UNIQUE PRIMARY KEY NOT NULL,
    source TEXT NOT NULL ,
    table_name TEXT NOT NULL
);

INSERT INTO sqlite_sequence values('user', 1000);
INSERT INTO databases values('local','local','Admin');
INSERT INTO tables values('city','local','city');