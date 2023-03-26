--11. Середній бал, який певний викладач ставить певному студентові.
SELECT  s.fullname, t.fullname, round(avg(g.grade), 2) AS avg_grade
FROM grades g  
LEFT JOIN students s ON s.id = g.student_id
LEFT JOIN disciplines d ON d.id = g.discipline_id
LEFT JOIN teachers t ON t.id = d.teacher_id
WHERE t.id = 1 AND s.id = 33
GROUP BY s.fullname, t.fullname;