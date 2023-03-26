from datetime import datetime, date, timedelta
from random import randint, choice

from faker import Faker
from psycopg2 import DatabaseError

from connect import create_connection


fake = Faker("uk-UA")

disciplines = [
    "Анатомія",
    "Фізіологія",
    "Медична фізика",
    "Біохімая",
    "Ділова українська мова",
    "Політологія",
    "Медична біологія",
    "Латинська мова",
    "Англійська мова",
    "Гістологія",
]

groups = ["I", "II", "III"]

NUMBERS_TEACHERS = 5
NUMBER_STUDENTS = 40


def seed_teacher(c):
    teachers = [fake.name() for _ in range(NUMBERS_TEACHERS)]
    sql_ex = "INSERT INTO teachers(fullname) VALUES(%s);"
    c.executemany(
        sql_ex,
        zip(
            teachers,
        ),
    )


def seed_groups(c):
    sql_ex = "INSERT INTO groups(name) VALUES(%s);"
    c.executemany(
        sql_ex,
        zip(
            groups,
        ),
    )


def seed_disciplines(c):
    list_teacher_id = [randint(1, NUMBERS_TEACHERS) for _ in range(len(disciplines))]
    sql_ex = "INSERT INTO disciplines(name, teacher_id) VALUES(%s, %s);"
    c.executemany(sql_ex, zip(disciplines, iter(list_teacher_id)))


def seed_students(c):
    students = [fake.name() for _ in range(NUMBER_STUDENTS)]
    list_group_id = [randint(1, len(groups)) for _ in range(NUMBER_STUDENTS)]
    sql_ex = "INSERT INTO students(fullname, group_id) VALUES(%s, %s);"
    c.executemany(sql_ex, zip(students, iter(list_group_id)))


def seed_grades(c):
    start_date = datetime.strptime("2022-09-01", "%Y-%m-%d")
    end_date = datetime.strptime("2023-06-30", "%Y-%m-%d")

    sql_ex = "INSERT INTO grades(student_id, discipline_id, grade, date_of) VALUES(%s, %s, %s, %s);"

    def get_list_of_date(start_date, end_date):
        result = []
        current_date: date = start_date
        while current_date <= end_date:
            if current_date.isoweekday() < 6:
                result.append(current_date)
            current_date += timedelta(1)
        return result

    list_dates = get_list_of_date(start_date, end_date)

    grades_data = []
    for student in range(1, NUMBER_STUDENTS+1):
        for _ in range(20):
            random_discipline = randint(1, len(disciplines))
            random_date = choice(list_dates)
            grades_data.append((student, random_discipline, randint(1, 12), random_date.date()))
    c.executemany(sql_ex, grades_data)


if __name__ == "__main__":
    with create_connection() as conn:
        if conn is not None:
            try:
                c = conn.cursor()
                seed_teacher(c)
                seed_groups(c)
                seed_disciplines(c)
                seed_students(c)
                seed_grades(c)
                c.close()
            except DatabaseError as e:
                print(e)
