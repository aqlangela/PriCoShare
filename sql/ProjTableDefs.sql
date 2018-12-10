CREATE TABLE Person(
    email VARCHAR(50),
    password CHAR(64),
    fname VARCHAR(20),
    lname VARCHAR(20),
    PRIMARY KEY (email)
);

CREATE TABLE Friendgroup(
    owner_email VARCHAR(50),
    fg_name VARCHAR(20),
    description VARCHAR(1000),
    PRIMARY KEY (owner_email, fg_name),
    FOREIGN KEY (owner_email) REFERENCES Person(email)
);


CREATE TABLE Belong (
    email VARCHAR(50),
    owner_email VARCHAR(50),
    fg_name VARCHAR(20),
    PRIMARY KEY (email, owner_email, fg_name),
    FOREIGN KEY(email) REFERENCES Person(email),
    FOREIGN KEY(owner_email, fg_name) REFERENCES  Friendgroup(owner_email, fg_name)
);

--- Modified

CREATE TABLE ContentItem(
    item_id int AUTO_INCREMENT,
    email_post VARCHAR(50),
    post_time Timestamp,
    event_name VARCHAR(40),
    event_description VARCHAR(400),
    event_date VARCHAR(40),
    event_location VARCHAR(40),
    is_pub Boolean,
    PRIMARY KEY(item_id),
    FOREIGN KEY(email_post) REFERENCES Person(email)
);

CREATE TABLE Rate (
    email VARCHAR(20),
    item_id int,
    rate_time Timestamp,
    emoji VARCHAR(20) CHARACTER SET utf8mb4,
    PRIMARY KEY(email, item_id),
    FOREIGN KEY(email) REFERENCES Person(email),
        FOREIGN KEY(item_id)REFERENCES ContentItem(item_id)
);

CREATE TABLE Share (
    owner_email VARCHAR(50),
    fg_name VARCHAR(20),
    item_id int,
    PRIMARY KEY(owner_email, fg_name, item_id),
    FOREIGN KEY(owner_email, fg_name) REFERENCES Friendgroup(owner_email, fg_name),
    FOREIGN KEY (item_id) REFERENCES ContentItem(item_id)
);

CREATE TABLE Tag (
    email_tagged VARCHAR(50),
    email_tagger VARCHAR(50),
    item_id int,
    status VARCHAR(20),
    tagtime Timestamp,
    PRIMARY KEY(email_tagged, email_tagger, item_id),
    FOREIGN KEY(email_tagged) REFERENCES Person(email),
    FOREIGN KEY(email_tagger) REFERENCES Person(email),
    FOREIGN KEY(item_id) REFERENCES ContentItem(item_id)
);

--- New Table

CREATE TABLE Signup (
    item_id int NOT NULL,
    email_signed VARCHAR(50) NOT NULL,
    PRIMARY KEY(item_id, email_signed),
    FOREIGN KEY(email_signed) REFERENCES Person(email),
    FOREIGN KEY(item_id) REFERENCES ContentItem(item_id)
)
