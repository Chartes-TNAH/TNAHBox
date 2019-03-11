INSERT INTO Person(
name, firstname, status)
-- email, login, passwordHash, linkedIn, cv
VALUES
("Pinche","Ariane","Enseignant·e"),
("Jolivet","Vincent","Enseignant·e"),
("Clérice","Thibault","Enseignant·e"),
("Verdese","Vincent","Enseignant·e"),
("Schmied","Marie-Caroline","Étudiant·e"),
("","Tony","autre");

INSERT INTO Document(
label, format, teaching)
-- date, downloadLink
VALUES
("doc1","pdf","XML TEI"),
("doc2","jpg","SQL"),
("doc3","odt","Python");

INSERT INTO Authorship(
userID, docuID)
VALUES
(5,1),
(5,2),
(3,3);

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