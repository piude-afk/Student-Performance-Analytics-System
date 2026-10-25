
USE student_analytics;

INSERT INTO departments (department_id, department_name)
VALUES
(1, 'Computer Science'),
(2, 'Information Technology'),
(3, 'Electronics'),
(4, 'Mechanical');

INSERT INTO subjects (subject_id, subject_name)
VALUES
(101, 'Python'),
(102, 'Database Management'),
(103, 'Statistics'),
(104, 'Data Analytics'),
(105, 'Computer Networks'),
(106, 'Mathematics');


INSERT INTO students
(student_id, student_name, email, department_id, semester)
VALUES
(1001, 'Aarav Sharma', 'aarav1001@example.com', 1, 6),
(1002, 'Ananya Das', 'ananya1002@example.com', 1, 6),
(1003, 'Rohan Roy', 'rohan1003@example.com', 1, 5),
(1004, 'Priya Sen', 'priya1004@example.com', 1, 6),
(1005, 'Arjun Dey', 'arjun1005@example.com', 1, 4),
(1006, 'Ishita Paul', 'ishita1006@example.com', 1, 6),
(1007, 'Rahul Ghosh', 'rahul1007@example.com', 1, 5),
(1008, 'Sneha Bose', 'sneha1008@example.com', 1, 6),

(1009, 'Aditya Roy', 'aditya1009@example.com', 2, 6),
(1010, 'Riya Das', 'riya1010@example.com', 2, 5),
(1011, 'Sayan Mitra', 'sayan1011@example.com', 2, 6),
(1012, 'Meera Dutta', 'meera1012@example.com', 2, 4),
(1013, 'Kunal Pal', 'kunal1013@example.com', 2, 6),
(1014, 'Diya Sen', 'diya1014@example.com', 2, 5),
(1015, 'Ayan Ghosh', 'ayan1015@example.com', 2, 6),
(1016, 'Nisha Roy', 'nisha1016@example.com', 2, 6),

(1017, 'Soham Das', 'soham1017@example.com', 3, 6),
(1018, 'Tanya Paul', 'tanya1018@example.com', 3, 5),
(1019, 'Abir Bose', 'abir1019@example.com', 3, 6),
(1020, 'Moumita Dey', 'moumita1020@example.com', 3, 4),
(1021, 'Ritwik Sen', 'ritwik1021@example.com', 3, 6),
(1022, 'Srija Roy', 'srija1022@example.com', 3, 5),
(1023, 'Debjit Pal', 'debjit1023@example.com', 3, 6),

(1024, 'Kavya Sharma', 'kavya1024@example.com', 4, 6),
(1025, 'Vivek Das', 'vivek1025@example.com', 4, 5),
(1026, 'Pallavi Roy', 'pallavi1026@example.com', 4, 6),
(1027, 'Sourav Dey', 'sourav1027@example.com', 4, 4),
(1028, 'Aditi Bose', 'aditi1028@example.com', 4, 6),
(1029, 'Manish Sen', 'manish1029@example.com', 4, 5),
(1030, 'Tithi Ghosh', 'tithi1030@example.com', 4, 6);


INSERT INTO marks (student_id, subject_id, marks)
SELECT
    s.student_id,
    sub.subject_id,
    MOD(s.student_id * 7 + sub.subject_id * 3, 61) + 35
FROM students s
CROSS JOIN subjects sub;


SELECT COUNT(*) AS total_departments
FROM departments;

SELECT COUNT(*) AS total_subjects
FROM subjects;

SELECT COUNT(*) AS total_students
FROM students;

SELECT COUNT(*) AS total_marks_records
FROM marks;


SELECT
    s.student_id,
    s.student_name,
    COUNT(m.subject_id) AS subject_count
FROM students s
LEFT JOIN marks m
    ON s.student_id = m.student_id
GROUP BY s.student_id, s.student_name
ORDER BY s.student_id;


SELECT
    s.student_id,
    s.student_name,
    d.department_name,
    sub.subject_name,
    m.marks
FROM marks m
JOIN students s
    ON m.student_id = s.student_id
JOIN departments d
    ON s.department_id = d.department_id
JOIN subjects sub
    ON m.subject_id = sub.subject_id
ORDER BY s.student_id, sub.subject_id;








