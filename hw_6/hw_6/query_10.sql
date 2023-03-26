--10. Список курсів, які певному студенту читає певний викладач.
SELECT s.fullname, t.fullname, d.name 
FROM grades g  
LEFT JOIN students s ON s.id = g.student_id
LEFT JOIN disciplines d ON d.id = g.discipline_id
LEFT JOIN teachers t ON t.id = d.teacher_id
WHERE t.id = 1 AND g.student_id = 29
GROUP BY d.name, s.fullname, t.fullname;
