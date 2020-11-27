CREATE TABLE IF NOT EXISTS site_menu(
	id integer PRIMARY KEY AUTOINCREMENT,
	title text NOT NULL,
	url text NOT NULL
);

CREATE TABLE IF NOT EXISTS articles (
	id integer PRIMARY KEY AUTOINCREMENT,
	title text NOT NULL,
	content text NOT NULL,
	url text NOT NULL,
	creation_date integer NOT NULL
);

CREATE TABLE IF NOT EXISTS users (
    id integer PRIMARY KEY AUTOINCREMENT,
    name text NOT NULL,
    email text NOT NULL,
    password text NOT NULL,
    user_avatar BLOB DEFAULT NULL,
    time integer NOT NULL
);


