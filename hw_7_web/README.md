The CLI program can work with the following action Commands: create, list, update, remove.
-h parameter returns the list of available parameters

Program accepts names, not ids.

For example, if you need to update some teacher's name, you go:
-a update -m Teacher -n 'Кирило Дрозд' --new_name 'Галина Журавель'

For models(Teacher, Student, Groups, Disciplines) you can change any Column
For Grade model you can change only grade Column if it is found by Grade.date_of, Student.fullname, Discipline.name

When creating the new Teacher, Student models you can skip the name parameter and it will get a random fake name

When creating Student model you can skip also the group_id parameter and it will be randomly assigned to any existing group

When creating Discipline model you can skip the teacher_id parameter and it will be randomly assigned to any existing teacher

To create a new Grade you need to enter all parameters: grade; date_of in a format "%Y-%m-%d"; Student.fullname, Discipline.name