DROP TABLE users

CREATE TABLE users (id INTEGER PRIMARY KEY, username TEXT, hash TEXT);

CREATE TABLE watchlist_requests (request_id SERIAL PRIMARY KEY UNIQUE NOT NULL, ticker TEXT, user_id INTEGER);