from sqlalchemy import func, desc, select, and_

from database.models import Teacher, Student, Discipline, Grade, Group
from database.db import session


def select_1():
    """
    1. Знайти 5 студентів із найбільшим середнім балом з усіх предметів.
    SELECT s.fullname, ROUND(AVG(g.grade), 2) as avg_grade
    FROM grades g
    LEFT JOIN students s ON s.id = g.student_id
    GROUP BY s.id
    ORDER BY avg_grade DESC
    LIMIT 5;
    :return:
    """
    result = (
        session.query(
            Student.fullname, func.round(func.avg(Grade.grade), 2).label("avg_grade")
        )
        .select_from(Grade)
        .join(Student)
        .group_by(Student.id)
        .order_by(desc("avg_grade"))
        .limit(5)
        .all()
    )
    return result


def select_2():
    """
    2. Знайти студента із найвищим середнім балом з певного предмета.
    SELECT d.name, s.fullname, ROUND(AVG(g.grade), 2) as avg_grade
    FROM grades g
    LEFT JOIN students s ON s.id = g.student_id
    LEFT JOIN disciplines d ON d.id = g.discipline_id
    WHERE d.id = 5
    GROUP BY s.id
    ORDER BY avg_grade DESC
    LIMIT 1;
    :return:
    """
    result = (
        session.query(
            Discipline.name,
            Student.fullname,
            func.round(func.avg(Grade.grade), 2).label("avg_grade"),
        )
        .select_from(Grade)
        .join(Student)
        .join(Discipline)
        .filter(Discipline.id == 5)
        .group_by(Student.id, Discipline.name)
        .order_by(desc("avg_grade"))
        .limit(1)
        .first()
    )
    return result


def select_3():
    """
    3. Знайти середній бал у групах з певного предмета.
    SELECT d.name, gr.name, round(avg(g.grade), 2) AS avg_grade
    FROM grades g
    LEFT JOIN students s ON s.id = g.student_id
    LEFT JOIN disciplines d ON d.id = g.discipline_id
    LEFT JOIN groups gr ON gr.id = s.group_id
    WHERE d.id = 3
    GROUP BY gr.name, d.name
    ORDER BY avg_grade DESC;
    """
    result = (
        session.query(
            Discipline.name,
            Group.name,
            func.round(func.avg(Grade.grade), 2).label("avg_grade"),
        )
        .select_from(Grade)
        .join(Student)
        .join(Discipline)
        .join(Group)
        .filter(Discipline.id == 5)
        .group_by(Group.name, Discipline.name)
        .order_by(desc("avg_grade"))
        .all()
    )
    return result


def select_4():
    """
    4. Знайти середній бал на потоці (по всій таблиці оцінок).
    SELECT round(avg(g.grade), 2) AS avg_grade
    FROM grades g;
    """
    result = session.query(
        func.round(func.avg(Grade.grade), 2).label("avg_grade"),
    ).all()
    return result


def select_5():
    """
    5. Знайти які курси читає певний викладач.
    SELECT d.id, t.fullname, d.name
    FROM teachers t
    LEFT JOIN disciplines d ON t.id = d.teacher_id
    WHERE t.id = 4;
    """
    result = (
        session.query(Discipline.id, Teacher.fullname, Discipline.name)
        .select_from(Teacher)
        .join(Discipline)
        .filter(Teacher.id == 4)
        .all()
    )
    return result


def select_6():
    """
    6. Знайти список студентів у певній групі.
    SELECT s.id, s.fullname, gr.name
    FROM students s
    LEFT JOIN groups gr ON gr.id = s.group_id
    WHERE gr.id = 3;
    """
    result = (
        session.query(Student.id, Student.fullname, Group.name)
        .select_from(Student)
        .join(Group)
        .filter(Group.id == 3)
        .all()
    )
    return result


def select_7():
    """
    7. Знайти оцінки студентів у окремій групі з певного предмета.
    SELECT s.id, d.name, gr.name, s.fullname, g.grade, g.date_of
    FROM grades g
    LEFT JOIN students s ON s.id = g.student_id
    LEFT JOIN disciplines d ON d.id = g.discipline_id
    LEFT JOIN groups gr ON gr.id = s.group_id
    WHERE d.id = 3 AND gr.id = 3;
    """
    result = (
        session.query(
            Student.id,
            Discipline.name,
            Group.name,
            Student.fullname,
            Grade.grade,
            Grade.date_of,
        )
        .select_from(Grade)
        .join(Student)
        .join(Discipline)
        .join(Group)
        .filter(and_(Discipline.id == 3, Group.id == 3))
        .all()
    )
    return result


def select_8():
    """
    8. Знайти середній бал, який ставить певний викладач зі своїх предметів.
    SELECT t.fullname, round(avg(g.grade), 2) AS avg_grade
    FROM grades g
    LEFT JOIN disciplines d ON d.id = g.discipline_id
    LEFT JOIN teachers t ON t.id = d.teacher_id
    WHERE t.id = 4
    GROUP BY t.fullname;
    """
    result = (
        session.query(
            Teacher.fullname,
            func.round(func.avg(Grade.grade), 2).label("avg_grade"),
        )
        .select_from(Grade)
        .join(Discipline)
        .join(Teacher)
        .filter(Teacher.id == 4)
        .group_by(Teacher.fullname)
        .first()
    )
    return result


def select_9():
    """
    9. Знайти список курсів, які відвідує студент.
    SELECT d.name, s.fullname
    FROM grades g
    LEFT JOIN students s ON s.id = g.student_id
    LEFT JOIN disciplines d ON d.id = g.discipline_id
    WHERE g.student_id = 19
    GROUP BY d.name, s.fullname;
    """
    result = (
        session.query(Discipline.name, Student.fullname)
        .select_from(Grade)
        .join(Student)
        .join(Discipline)
        .filter(Grade.student_id == 19)
        .group_by(Discipline.name, Student.fullname)
        .all()
    )
    return result


def select_10():
    """
    10. Список курсів, які певному студенту читає певний викладач.
    SELECT s.fullname, t.fullname, d.name
    FROM grades g
    LEFT JOIN students s ON s.id = g.student_id
    LEFT JOIN disciplines d ON d.id = g.discipline_id
    LEFT JOIN teachers t ON t.id = d.teacher_id
    WHERE t.id = 4 AND g.student_id = 33
    GROUP BY d.name, s.fullname, t.fullname;
    """
    result = (
        session.query(Student.fullname, Teacher.fullname, Discipline.name)
        .select_from(Grade)
        .join(Student)
        .join(Discipline)
        .join(Teacher)
        .filter(and_(Teacher.id == 4, Grade.student_id == 33))
        .group_by(Discipline.name, Student.fullname, Teacher.fullname)
        .all()
    )
    return result


def select_add_1():
    """
    11. Середній бал, який певний викладач ставить певному студентові.
    SELECT  s.fullname, t.fullname, round(avg(g.grade), 2) AS avg_grade
    FROM grades g
    LEFT JOIN students s ON s.id = g.student_id
    LEFT JOIN disciplines d ON d.id = g.discipline_id
    LEFT JOIN teachers t ON t.id = d.teacher_id
    WHERE t.id = 4 AND s.id = 33
    GROUP BY s.fullname, t.fullname;
    """
    result = (
        session.query(
            Student.fullname,
            Teacher.fullname,
            func.round(func.avg(Grade.grade), 2).label("avg_grade"),
        )
        .select_from(Grade)
        .join(Student)
        .join(Discipline)
        .join(Teacher)
        .filter(and_(Teacher.id == 4, Student.id == 33))
        .group_by(Student.fullname, Teacher.fullname)
        .first()
    )
    return result


def select_add_2():
    """
    12. Оцінки студентів у певній групі з певного предмета на останньому занятті.
    SELECT s.id, s.fullname, g.grade, g.date_of
    FROM grades g
    JOIN students s on s.id = g.student_id
    WHERE g.discipline_id = 3 and s.group_id = 3 and g.date_of = (
        SELECT max(date_of)
        FROM grades g2
        JOIN students s2 on s2.id = g2.student_id
        WHERE g2.discipline_id = 3 and s2.group_id = 3;
    """
    subquery = (
        select(func.max(Grade.date_of))
        .join(Student)
        .filter(and_(Grade.discipline_id == 3, Student.group_id == 3))
        .scalar_subquery()
    )

    result = (
        session.query(Student.id, Student.fullname, Grade.grade, Grade.date_of)
        .select_from(Grade)
        .join(Student)
        .filter(
            and_(
                Grade.discipline_id == 3,
                Student.group_id == 3,
                Grade.date_of == subquery,
            )
        )
        .all()
    )
    return result


if __name__ == "__main__":
    # print(select_1())
    # print(select_2())
    # print(select_3())
    # print(select_4())
    # print(select_5())
    # print(select_6())
    # print(select_7())
    # print(select_8())
    # print(select_9())
    # print(select_10())
    # print(select_add_1())
    print(select_add_2())
