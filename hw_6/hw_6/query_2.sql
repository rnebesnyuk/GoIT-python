--2. Знайти студента із найвищим середнім балом з певного предмета.
SELECT d.name, s.fullname, round(avg(g.grade), 2) AS avg_grade 
FROM grades g 
LEFT JOIN students s ON s.id = g.student_id
LEFT JOIN disciplines d ON d.id = g.discipline_id
WHERE d.id = 1
GROUP BY s.fullname, d.name
ORDER BY avg_grade DESC
LIMIT 1;