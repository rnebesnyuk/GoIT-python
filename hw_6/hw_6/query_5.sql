--5. Знайти які курси читає певний викладач.
SELECT d.id, t.fullname, d.name 
FROM teachers t 
LEFT JOIN disciplines d ON t.id = d.teacher_id
WHERE t.id = 3;