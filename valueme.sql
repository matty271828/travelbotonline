DROP TABLE users

CREATE TABLE users (id INTEGER PRIMARY KEY, username TEXT, hash TEXT);

CREATE TABLE watchlist_requests (request_id SERIAL PRIMARY KEY, ticker TEXT, user_id INTEGER);