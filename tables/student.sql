CREATE TABLE Students (
    id INT NOT NULL AUTO_INCREMENT,
    first_name VARCHAR(255) NOT NULL,
    last_name VARCHAR(255) NOT NULL,
    PRIMARY KEY (id)
);

CREATE TABLE Courses (
    id INT NOT NULL AUTO_INCREMENT,
    name VARCHAR(255) NOT NULL,
    PRIMARY KEY (id)
);

CREATE TABLE EnrolmentDates (
    id INT NOT NULL AUTO_INCREMENT,
    date DATE NOT NULL,
    PRIMARY KEY (id),
    UNIQUE (date)
);

CREATE TABLE Enrolments (
    id INT NOT NULL AUTO_INCREMENT,
    student_id INT NOT NULL,
    course_id INT NOT NULL,
    date_id INT NOT NULL,
    PRIMARY KEY (id),
    FOREIGN KEY (student_id) REFERENCES Students(id),
    FOREIGN KEY (course_id) REFERENCES Courses(id),
    FOREIGN KEY (date_id) REFERENCES EnrolmentDates(id)
);