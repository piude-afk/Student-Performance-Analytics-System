
CREATE DATABASE IF NOT EXISTS student_analytics;

USE student_analytics;

CREATE TABLE departments (
    department_id INT PRIMARY KEY,
    department_name VARCHAR(100) NOT NULL UNIQUE
);


CREATE TABLE students (
    student_id INT PRIMARY KEY,
    student_name VARCHAR(100) NOT NULL,
    email VARCHAR(150) NOT NULL UNIQUE,
    department_id INT NOT NULL,
    semester INT NOT NULL DEFAULT 1,

    CONSTRAINT fk_student_department
        FOREIGN KEY (department_id)
        REFERENCES departments(department_id),

    CONSTRAINT chk_student_semester
        CHECK (semester BETWEEN 1 AND 8)
);

CREATE TABLE subjects (
    subject_id INT PRIMARY KEY,
    subject_name VARCHAR(100) NOT NULL UNIQUE
);


CREATE TABLE marks (
    student_id INT NOT NULL,
    subject_id INT NOT NULL,
    marks DECIMAL(5,2) NOT NULL DEFAULT 0,

    PRIMARY KEY (student_id, subject_id),

    CONSTRAINT fk_marks_student
        FOREIGN KEY (student_id)
        REFERENCES students(student_id),

    CONSTRAINT fk_marks_subject
        FOREIGN KEY (subject_id)
        REFERENCES subjects(subject_id),

    CONSTRAINT chk_marks_range
        CHECK (marks BETWEEN 0 AND 100)
);


USE student_analytics;

SHOW TABLES;


USE student_analytics;

SELECT DATABASE();


DESCRIBE departments;
DESCRIBE students;
DESCRIBE subjects;
DESCRIBE marks;

SELECT VERSION();


USE student_analytics;

SHOW CREATE TABLE students;
SHOW CREATE TABLE marks;




