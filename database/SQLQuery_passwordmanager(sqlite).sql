
/*DROP TABLE userdata
DROP TABLE usersaves*/

CREATE TABLE UserData (
	user_id INTEGER NOT NULL,
	email TEXT NOT NULL UNIQUE,
	salt BLOB NOT NULL,
	iv BLOB NOT NULL,
	mcvalue BLOB NOT NULL,
	cvalue BLOB NOT NULL,
	emk BLOB NOT NULL,
	PRIMARY KEY(user_id))
	
CREATE TABLE Entity (
	entity_id	INTEGER NOT NULL,
	entity_name TEXT NOT NULL,
	entity_un	BLOB NOT NULL,
	entity_pw	BLOB NOT NULL,
	note TEXT,
	PRIMARY KEY(entity_id))
	
CREATE TABLE User_Entity(
	user_id INT NOT NULL,
	entity_id INT NOT NULL,
	PRIMARY KEY (user_id, entity_id),
	FOREIGN KEY (user_id) REFERENCES UserData(user_id),
	FOREIGN KEY (entity_id) REFERENCES Entity(entity_id))