--8. Знайти середній бал, який ставить певний викладач зі своїх предметів.
SELECT t.fullname, round(avg(g.grade), 2) AS avg_grade
FROM grades g  
LEFT JOIN disciplines d ON d.id = g.discipline_id
LEFT JOIN teachers t ON t.id = d.teacher_id
WHERE t.id = 4
GROUP BY t.fullname;