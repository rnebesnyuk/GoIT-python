from datetime import datetime, date, timedelta
from random import randint, choice

from faker import Faker
from sqlalchemy import select

from database.models import Teacher, Student, Discipline, Grade, Group
from database.db import session


def fill_data():
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

    NUMBER_OF_TEACHERS = 5
    NUMBER_OF_STUDENTS = 40

    def seed_teacher():
        for _ in range(NUMBER_OF_TEACHERS):
            teacher = Teacher(fullname=fake.name())
            session.add(teacher)
        session.commit()

    def seed_groups():
        for group in groups:
            session.add(Group(name=group))
        session.commit()

    def seed_disciplines():
        list_teacher_id = session.scalars(select(Teacher.id)).all()
        for discipline in disciplines:
            session.add(Discipline(name=discipline, teacher_id=choice(list_teacher_id)))
        session.commit()

    def seed_students():
        list_group_id = session.scalars(select(Group.id)).all()
        for _ in range(NUMBER_OF_STUDENTS):
            student = Student(fullname=fake.name(), group_id=choice(list_group_id))
            session.add(student)
        session.commit()

    def seed_grades():
        start_date = datetime.strptime("2022-09-01", "%Y-%m-%d")
        end_date = datetime.strptime("2023-06-30", "%Y-%m-%d")

        def get_list_of_date(start_date, end_date):
            result = []
            current_date: date = start_date
            while current_date <= end_date:
                if current_date.isoweekday() < 6:
                    result.append(current_date)
                current_date += timedelta(1)
            return result

        list_dates = get_list_of_date(start_date, end_date)

        for student in range(1, NUMBER_OF_STUDENTS + 1):
            for _ in range(20):
                random_discipline = randint(1, len(disciplines))
                random_date = choice(list_dates)
                grade = Grade(
                    grade=randint(1, 12),
                    date_of=random_date,
                    student_id=student,
                    discipline_id=random_discipline,
                )
                session.add(grade)
        session.commit()

    seed_teacher()
    seed_groups()
    seed_disciplines()
    seed_students()
    seed_grades()


if __name__ == "__main__":
    fill_data()
