INSERT INTO Person(
person_name, person_firstname, person_is_teacher, person_promotion)
-- person_email, 
-- person_login, person_password, person_linkedIn,
-- person_cv, person_git, person_is_admin
VALUES
("Pinche","Ariane", 1, "2014"),
("Jolivet","Vincent", 1, ""),
("Clérice","Thibault", 1, "2014"),
("Andrieux","Clément", 0, "2019"),
("Schmied","Marie-Caroline", 0, "2019"),
("","Tony", 0, "");

INSERT INTO Document(
document_title, document_format, document_teaching, document_date, document_description)
-- document_downloadLink
VALUES
("doc1","autre","XML TEI","2018-11-23","Présentation des TEI Guidelines"),
("doc2","texte","SQL","2018-12-12","Tuto MySQL Workbench"),
("doc3","code","Python","2019-03-01","Correction du devoir sur table"),
("doc4","texte","XML EAD","2019-01","Retroconvertion de l'instrument de recherche du fonds Emile Portzer"),
("doc5","image","CMS","2018","Schéma d'un CMS comme Omeka"),
("doc6","code","LaTeX","2018-11-13","Template de présentation du mémoire de M2");

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