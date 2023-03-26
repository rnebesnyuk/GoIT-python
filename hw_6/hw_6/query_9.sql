--9. Знайти список курсів, які відвідує студент.
SELECT d.name, s.fullname 
FROM grades g 
LEFT JOIN students s ON s.id = g.student_id
LEFT JOIN disciplines d ON d.id = g.discipline_id
WHERE g.student_id = 13
GROUP BY d.name, s.fullname;