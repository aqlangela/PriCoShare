INSERT INTO Person VALUES ('AA@nyu.edu', SHA2('AA', 256), 'Ann', 'Anderson');
INSERT INTO Person VALUES ('BB@nyu.edu', SHA2('BB', 256), 'Bob', 'Baker');
INSERT INTO Person VALUES ('CC@nyu.edu', SHA2('CC', 256), 'Cathy', 'Chang');
INSERT INTO Person VALUES ('DD@nyu.edu', SHA2('DD', 256), 'David', 'Davidson');
INSERT INTO Person VALUES ('EE@nyu.edu', SHA2('EE', 256), 'Ellen', 'Ellenberg');
INSERT INTO Person VALUES ('FF@nyu.edu', SHA2('FF', 256), 'Fred', 'Fox');
INSERT INTO Person VALUES ('GG@nyu.edu', SHA2('GG', 256), 'Gina', 'Gupta');
INSERT INTO Person VALUES ('HH@nyu.edu', SHA2('HH', 256), 'Helen', 'Haper');

-- Ann owns FriendGroup called “family” with users Ann, Cathy, David, and Ellen.

INSERT INTO FriendGroup VALUES ('AA@nyu.edu','family',  '');
INSERT INTO Belong VALUES ('AA@nyu.edu','AA@nyu.edu','family' );
INSERT INTO Belong VALUES ('CC@nyu.edu','AA@nyu.edu','family');
INSERT INTO Belong VALUES ('DD@nyu.edu', 'AA@nyu.edu' ,'family');
INSERT INTO Belong VALUES ('EE@nyu.edu', 'AA@nyu.edu','family' );

-- Bob owns FriendGroup called “family” with users Bob, Fred, and Ellen.

INSERT INTO FriendGroup VALUES ('BB@nyu.edu','family',  '');
INSERT INTO Belong VALUES ( 'BB@nyu.edu','BB@nyu.edu','family');
INSERT INTO Belong VALUES ( 'FF@nyu.edu','BB@nyu.edu','family');
INSERT INTO Belong VALUES ( 'EE@nyu.edu','BB@nyu.edu','family');

-- Ann owns FriendGroup called “roommates” with users Ann, Gina, and Helen.

INSERT INTO FriendGroup VALUES ('AA@nyu.edu','roommates',  '');
INSERT INTO Belong VALUES ('AA@nyu.edu', 'AA@nyu.edu','roommates' );
INSERT INTO Belong VALUES ('GG@nyu.edu', 'AA@nyu.edu','roommates' );
INSERT INTO Belong VALUES ('HH@nyu.edu', 'AA@nyu.edu','roommates' );

-- Ann posted a content item with item_ID=1, item_name = “Views from NYU Taping feat”, is pub = False, and shared it with her “family” FriendGroup.

INSERT INTO `ContentItem` VALUES ('1', 'AA@nyu.edu', CURRENT_TIMESTAMP, 'Views from NYU Taping feat', 'Don\'t miss this semester\'s taping of Views from NYU, a new variety show created to showcase NYU talent.Hosted by Brandon Lew, Views features comedy, music, and other talent from the NYU community. Our headliner guests for the Fall 2018 semester\'s taping will be comedian/impressionist Matthew Friend and singer/dancer Sam Guyton. Sam will be debuting his first-ever single on the show.', '12.21', 'Kimmel Center for University Life', '1');

-- Ann posted a content item with item_ID=2, item_name = “leftovers in fridge”, is pub = False, and shared it with her “roommates” FriendGroup.

INSERT INTO `ContentItem`  VALUES ('2', 'AA@nyu.edu', CURRENT_TIMESTAMP, 'Leftovers in fridge', 'Let\'s clean the leftovers in fridge', '11.21', 'dorm', '0');
INSERT INTO Share VALUES ('AA@nyu.edu','roommates',  '2');

INSERT INTO `ContentItem` VALUES ('3', 'AA@nyu.edu', CURRENT_TIMESTAMP, 'Picnic', '', '11.22', 'Central Park', '0');
INSERT INTO Share VALUES ('AA@nyu.edu','family',  '3');

Insert into Tag values("AA@nyu.edu","CC@nyu.edu","3","True",CURRENT_TIMESTAMP);
Insert into Tag values("EE@nyu.edu","AA@nyu.edu","1","True",CURRENT_TIMESTAMP);

Insert into Rate values("AA@nyu.edu","3",CURRENT_TIMESTAMP,"^_^");
Insert into Rate values("EE@nyu.edu","1",CURRENT_TIMESTAMP,":)");
