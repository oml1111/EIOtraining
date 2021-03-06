CREATE TABLE users (user VARCHAR(20), INDEX(user), password_hash TEXT, salt VARCHAR(20), id BIGINT, INDEX(id), email TEXT, privilige TINYINT);
CREATE TABLE variables (name VARCHAR(20), value BIGINT);
CREATE TABLE news (title VARCHAR(255), content MEDIUMTEXT, id BIGINT, INDEX(id), created DATETIME, INDEX(created), creator_id BIGINT, INDEX(creator_id) );
CREATE TABLE navlinks (parent BIGINT, INDEX(parent), id BIGINT, INDEX(id), type TINYINT, description VARCHAR(255));
CREATE TABLE statements (parent BIGINT, INDEX(parent), statement TEXT, type TINYINT);