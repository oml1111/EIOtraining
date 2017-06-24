CREATE PROCEDURE signup (user VARCHAR(20), password_hash TEXT, salt VARCHAR(20), id BIGINT, email TEXT)
BEGIN
	INSERT INTO users VALUES(user, password_hash, salt, id, email, 0);
END