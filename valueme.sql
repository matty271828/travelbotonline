DROP TABLE users

CREATE TABLE users (
	id SERIAL PRIMARY KEY,
	username TEXT,
	hash TEXT,
);