INSERT INTO Person(
person_name, person_firstname, person_is_teacher, person_promotion)
-- person_email, 
-- person_login, person_password, person_linkedIn,
-- person_cv, person_git, person_is_admin
VALUES
("Pinche","Ariane", 1, "2013-2014"),
("Jolivet","Vincent", 1, ""),
("Clérice","Thibault", 1, "2013-2014"),
("Andrieux","Clément", 0, "2018-2019"),
("Schmied","Marie-Caroline", 0, "2018-2019"),
("","Tony", 0, "");

INSERT INTO Document(
document_label, document_format, document_teaching)
-- document_date, document_description, document_downloadLink
VALUES
("doc1","pdf","XML TEI"),
("doc2","jpg","SQL"),
("doc3","odt","Python");

INSERT INTO Authorship(
authorship_person_id, authorship_document_id)
VALUES
(4,1),
(5,2),
(3,3);

INSERT INTO Tag(
tag_label)
VALUES
("teiHeader 4EVER"), 
("DROP TABLE *;"),
("Pythounou Coconut Root");

INSERT INTO HasTag(
hasTag_tag_id, hasTag_doc_id)
VALUES
(1,1), 
(2,2),
(3,3);