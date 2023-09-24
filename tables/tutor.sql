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

CREATE TABLE Enrolments (
    id INT NOT NULL AUTO_INCREMENT,
    student_id INT NOT NULL,
    date DATE NOT NULL,
    PRIMARY KEY (id),
    FOREIGN KEY (student_id) REFERENCES Students(id)
);

CREATE TABLE EnrolmentCourse (
    id INT NOT NULL AUTO_INCREMENT,
    enrolment_id INT NOT NULL,
    course_id INT NOT NULL,
    FOREIGN KEY (enrolment_id) REFERENCES Enrolments(id),
    FOREIGN KEY (course_id) REFERENCES Courses(id),
    PRIMARY KEY (id)
);