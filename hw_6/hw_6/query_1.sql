--1. Знайти 5 студентів із найбільшим середнім балом з усіх предметів.
SELECT s.fullname, round(avg(g.grade), 2) AS avg_grade 
FROM grades g 
LEFT JOIN students s ON s.id = g.student_id
GROUP BY s.fullname, s.id
ORDER BY avg_grade DESC
LIMIT 5;
