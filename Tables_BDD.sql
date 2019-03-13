CREATE TABLE IF NOT EXISTS Person (
person_id INTEGER PRIMARY KEY AUTOINCREMENT,
person_name TEXT NOT NULL,
person_firstName TEXT NOT NULL,
person_is_teacher INTEGER NULL,
person_promotion TEXT NULL,
person_email TEXT NULL,
person_login TEXT NULL,
person_password TEXT NULL,
person_linkedIn TEXT NULL,
person_cv TEXT NULL,
person_git TEXT NULL,
person_is_admin INTEGER NULL
);

CREATE TABLE IF NOT EXISTS Document (
document_id INTEGER PRIMARY KEY AUTOINCREMENT,
document_title TEXT NOT NULL,
document_description TEXT NULL,
document_format TEXT NULL,
document_date TEXT NULL,
document_teaching TEXT NULL,
document_downloadLink TEXT NULL
); 

CREATE TABLE IF NOT EXISTS Authorship (
authorship_person_id,
authorship_document_id,
authorship_date TEXT NULL,
PRIMARY KEY (authorship_person_id, authorship_document_id),
FOREIGN KEY (authorship_person_id) REFERENCES Person(person_id)
ON DELETE CASCADE ON UPDATE CASCADE,
FOREIGN KEY (authorship_document_id) REFERENCES Document(document_id)
ON DELETE CASCADE ON UPDATE CASCADE
);

CREATE TABLE IF NOT EXISTS Tag (
tag_id INTEGER PRIMARY KEY AUTOINCREMENT,
tag_label TEXT NOT NULL UNIQUE
);

CREATE TABLE IF NOT EXISTS HasTag (
hasTag_tag_id,
hasTag_doc_id,
PRIMARY KEY (hasTag_tag_id, hasTag_doc_id),
FOREIGN KEY (hasTag_tag_id) REFERENCES Tag(tag_id)
ON DELETE CASCADE ON UPDATE CASCADE,
FOREIGN KEY (hasTag_doc_id) REFERENCES Document(document_id)
ON DELETE CASCADE ON UPDATE CASCADE
);