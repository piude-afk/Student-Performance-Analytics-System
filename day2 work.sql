USE student_analytics;

SELECT
    sub.subject_id,
    sub.subject_name,
    ROUND(AVG(m.marks), 2) AS average_marks,
    MAX(m.marks) AS highest_marks,
    MIN(m.marks) AS lowest_marks
FROM subjects sub
JOIN marks m
    ON sub.subject_id = m.subject_id
GROUP BY sub.subject_id, sub.subject_name
ORDER BY sub.subject_id;


WITH student_averages AS (
    SELECT
        s.student_id,
        s.student_name,
        s.department_id,
        AVG(m.marks) AS average_marks
    FROM students s
    JOIN marks m
        ON s.student_id = m.student_id
    GROUP BY
        s.student_id,
        s.student_name,
        s.department_id
),
ranked_students AS (
    SELECT
        sa.*,
        DENSE_RANK() OVER (
            PARTITION BY department_id
            ORDER BY average_marks DESC
        ) AS department_rank
    FROM student_averages sa
)
SELECT
    d.department_name,
    rs.student_id,
    rs.student_name,
    ROUND(rs.average_marks, 2) AS average_marks
FROM ranked_students rs
JOIN departments d
    ON rs.department_id = d.department_id
WHERE rs.department_rank = 1
ORDER BY d.department_name;


SELECT DISTINCT
    s.student_id,
    s.student_name,
    d.department_name
FROM students s
JOIN departments d
    ON s.department_id = d.department_id
JOIN marks m
    ON s.student_id = m.student_id
WHERE m.marks < 40
ORDER BY s.student_id;


SELECT
    d.department_id,
    d.department_name,
    ROUND(AVG(m.marks), 2) AS department_average
FROM departments d
LEFT JOIN students s
    ON d.department_id = s.department_id
LEFT JOIN marks m
    ON s.student_id = m.student_id
GROUP BY d.department_id, d.department_name
ORDER BY d.department_id;


DROP FUNCTION IF EXISTS get_grade;

DELIMITER $$

CREATE FUNCTION get_grade(p_marks DECIMAL(5,2))
RETURNS VARCHAR(2)
DETERMINISTIC
NO SQL
BEGIN
    RETURN CASE
        WHEN p_marks IS NULL THEN NULL
        WHEN p_marks >= 90 THEN 'A+'
        WHEN p_marks >= 80 THEN 'A'
        WHEN p_marks >= 70 THEN 'B'
        WHEN p_marks >= 60 THEN 'C'
        WHEN p_marks >= 40 THEN 'D'
        ELSE 'F'
    END;
END $$

DELIMITER ;


SELECT
    get_grade(95) AS grade_95,
    get_grade(85) AS grade_85,
    get_grade(75) AS grade_75,
    get_grade(65) AS grade_65,
    get_grade(45) AS grade_45,
    get_grade(25) AS grade_25;


DROP FUNCTION IF EXISTS get_percentage;

DELIMITER $$

CREATE FUNCTION get_percentage(p_student_id INT)
RETURNS DECIMAL(5,2)
READS SQL DATA
BEGIN
    DECLARE v_total DECIMAL(10,2);
    DECLARE v_count INT;

    SELECT
        COALESCE(SUM(marks), 0),
        COUNT(*)
    INTO v_total, v_count
    FROM marks
    WHERE student_id = p_student_id;

    IF v_count = 0 THEN
        RETURN 0.00;
    END IF;

    RETURN ROUND((v_total / (v_count * 100)) * 100, 2);
END $$

DELIMITER ;



SELECT
    student_id,
    student_name,
    get_percentage(student_id) AS percentage
FROM students
ORDER BY student_id;


DROP FUNCTION IF EXISTS get_result;

DELIMITER $$

CREATE FUNCTION get_result(p_student_id INT)
RETURNS VARCHAR(4)
READS SQL DATA
BEGIN
    DECLARE v_total_subjects INT;
    DECLARE v_failed_subjects INT;

    SELECT COUNT(*)
    INTO v_total_subjects
    FROM marks
    WHERE student_id = p_student_id;

    SELECT COUNT(*)
    INTO v_failed_subjects
    FROM marks
    WHERE student_id = p_student_id
      AND marks < 40;

    IF v_total_subjects = 0 OR v_failed_subjects > 0 THEN
        RETURN 'FAIL';
    ELSE
        RETURN 'PASS';
    END IF;
END $$

DELIMITER ;


SELECT
    student_id,
    student_name,
    get_percentage(student_id) AS percentage,
    get_result(student_id) AS result
FROM students
ORDER BY student_id;


INSERT INTO students
(student_id, student_name, email, department_id, semester)
VALUES
(2001, 'Test Student', 'aarav1001@example.com', 1, 6);


INSERT INTO students
(student_id, student_name, email, department_id, semester)
VALUES
(2002, 'Test Student', 'test2002@example.com', 1, 9);

INSERT INTO marks (student_id, subject_id, marks)
VALUES (1001, 101, 105);


INSERT INTO marks (student_id, subject_id, marks)
VALUES (1001, 101, 80);


INSERT INTO students
(student_id, student_name, email, department_id, semester)
VALUES
(2003, 'Test Student', 'test2003@example.com', 99, 6);

INSERT INTO students
(student_id, student_name, email, department_id, semester)
VALUES
(2004, NULL, 'test2004@example.com', 1, 6);


SELECT
    (SELECT COUNT(*) FROM departments) AS departments,
    (SELECT COUNT(*) FROM subjects) AS subjects,
    (SELECT COUNT(*) FROM students) AS students,
    (SELECT COUNT(*) FROM marks) AS marks_records;

SHOW FUNCTION STATUS
WHERE Db = 'student_analytics';






