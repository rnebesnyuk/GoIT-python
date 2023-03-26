--7. Знайти оцінки студентів у окремій групі з певного предмета.
SELECT s.id, d.name, gr.name, s.fullname, g.grade, g.date_of  
FROM grades g 
LEFT JOIN students s ON s.id = g.student_id
LEFT JOIN disciplines d ON d.id = g.discipline_id
LEFT JOIN groups gr ON gr.id = s.group_id  
WHERE d.id = 3 AND gr.id = 3;
