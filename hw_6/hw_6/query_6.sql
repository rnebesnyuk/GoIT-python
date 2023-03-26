--6. Знайти список студентів у певній групі.
SELECT s.id, s.fullname, gr.name
FROM students s 
LEFT JOIN groups gr ON gr.id = s.group_id 
WHERE gr.id = 3;