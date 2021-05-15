create table 'student' (
  'sID' integer primary key,
  'sName' text,
  'age' integer,
  'GPA' integer,
  'sizeHS' text
);

create table 'college' (
  'cName' integer primary key,
  'state' text,
  'enrolment' text
);

create table 'apply' (
  'sID' integer primary key,
  'cName' text,
  'major' text,
  'decision' text
);

INSERT INTO 'student' ('sID', 'sName', 'age', 'GPA','sizeHS') VALUES
(1, 'A', 15,1, 155),
(2, 'B', 11,1, 6545),
(3, 'C', 29,1, 16516),
(4, 'D', 50,1, 1515),
(5, 'E', 33,1, 200);

INSERT INTO 'apply' ('sID', 'cName', 'major', 'decision') VALUES
(1, 'ntu', 'CS', 'Y'),
(2, 'B', 11,1, 6545),
(3, 'C', 29,1, 16516),
(4, 'D', 50,1, 1515),
(5, 'E', 33,1, 200),