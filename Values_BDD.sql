INSERT INTO Person(
name, firstname, status)
-- email, username, passwordHash, linkedIn, cv
VALUES
("Pinche","Ariane","enseignant·e"),
("Jolivet","Vincent","enseignant·e"),
("Clérice","Thibault","enseignant·e"),
("Verdese","Vincent","enseignant·e"),
("Schmied","Marie-Caroline","étudiant·e"),
("","Tony","autre");

INSERT INTO Teaching(
label, persName, persFirstname)
VALUES
("XML TEI","Pinche","Ariane"),
("SQL","Jolivet","Vincent"),
("Javascript","Clérice","Thibault"),
("XML EAD","Verdese","Vincent"),
("Python","Clérice","Thibault");

INSERT INTO Document(
label, format, teachingID)
-- date, downloadLink
VALUES
("doc1","pdf","XML TEI"),
("doc2","jpg","SQL"),
("doc3","odt","Python");

INSERT INTO Authorship(
persName, persFirstname, docuID)
VALUES
("Schmied","Marie-Caroline",1),
("Schmied","Marie-Caroline",2),
("Clérice","Thibault",3);

INSERT INTO Tag(
label)
VALUES
("teiHeader 4EVER"), 
("DROP TABLE *;"),
("Pythounou Coconut Root");

INSERT INTO HasTag(
tagID, docuID)
VALUES
(1,1), 
(2,2),
(3,3);


----- RESET -----

DROP TABLE Person;
DROP TABLE Document; 
DROP TABLE Tag;
DROP TABLE Teaching;
DROP TABLE Authorship;
DROP TABLE HasTag;
