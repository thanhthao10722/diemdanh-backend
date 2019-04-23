CREATE TABLE Student
(
	MSSV NVARCHAR(50), primary key,
	FingerprintId NVARCHAR(500),
	Fullname NVARCHAR(max),
    Phonenumber NVARCHAR(12),
    
);


CREATE TABLE Course
(
	IDCourse INT primary key not null,
	CourseName NVARCHAR(max),
);

CREATE TABLE RegisteredCourse
(
	IDRCourse INT primary key not null,
	IDCourse INT,
    MSSV VARCHAR(50),
    FOREIGN KEY(IDCourse) REFERENCES Course(IDCourse),
    FOREIGN KEY(MSSV) REFERENCES Student(MSSV),
	Semester INT
);

CREATE TABLE ScheduledCourse
(
	IDSC INT primary key not null,
	IDRCourse  int ,
    FOREIGN KEY(IDRCourse) REFERENCES RegisteredCourse(Id),
	Room NVARCHAR(10),
    StartTime DATETIME,
    StopTime DATETIME,
    Date DATETIME,
);

CREATE TABLE RollCall
(
	ID INT primary key not null,
	IDSC int ,
     MSSV VARCHAR(50),
    FOREIGN KEY(IDSC) REFERENCES ScheduledCourse(Id),
    FOREIGN KEY(IDSC) REFERENCES Student(MSSV),
	Status NVARCHAR(50),
	Note NVARCHAR(max)
);



