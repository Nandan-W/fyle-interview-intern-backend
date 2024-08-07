-- Write query to find the number of grade A's given by the teacher who has graded the most assignments

WITH MaxGradingTeacher AS (
    SELECT teacher_id, COUNT(*) AS grading_count
    FROM assignments
    WHERE grade = 'A'
    GROUP BY teacher_id
    ORDER BY grading_count DESC
    LIMIT 1
)

SELECT COUNT(*) AS grade_A_count
FROM assignments a
JOIN MaxGradingTeacher mgt ON a.teacher_id = mgt.teacher_id
WHERE a.grade = 'A';
