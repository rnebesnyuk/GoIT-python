from datetime import datetime
from random import choice

from sqlalchemy import and_

from database.db import session
from database.models import Teacher, Student, Group, Grade, Discipline


def create_entry(model, name, group, teacher, grade, date_of, student, discipline):
    if model == "Teacher":
        entry = Teacher(fullname=name)
    elif model == "Student":
        if not group:
            list_of_groups = [Group.id for Group in session.query(Group)]
            entry = Student(fullname=name, group_id=choice(list_of_groups))
        else:
            group_id = session.query(Group.id).filter(Group.name == group).scalar()
            entry = Student(fullname=name, group_id=group_id)
    elif model == "Group":
        entry = Group(name=name)
    elif model == "Discipline":
        if not teacher:
            list_of_teachers = [Teacher.id for Teacher in session.query(Teacher)]
            entry = Discipline(name=name, teacher_id=choice(list_of_teachers))
        else:
            teacher_id = (
                session.query(Teacher.id).filter(Teacher.fullname == teacher).scalar()
            )
            entry = Discipline(name=name, teacher_id=teacher_id)
    elif model == "Grade":
        student_id = (
            session.query(Student.id).filter(Student.fullname == student).scalar()
        )
        discipline_id = (
            session.query(Discipline.id).filter(Discipline.name == discipline).scalar()
        )
        entry = Grade(
            grade=grade,
            date_of=datetime.strptime(date_of, "%Y-%m-%d"),
            student_id=student_id,
            discipline_id=discipline_id,
        )
    session.add(entry)
    session.commit()
    session.close()


def get_entries(model):
    if model == "Teacher":
        entries = session.query(Teacher).all()
        for row in entries:
            print(row.id, row.fullname)
    elif model == "Student":
        entries = session.query(Student).all()
        for row in entries:
            print(row.id, row.fullname, row.group_id)
    elif model == "Group":
        entries = session.query(Group).all()
        for row in entries:
            print(row.id, row.name)
    elif model == "Discipline":
        entries = session.query(Discipline).all()
        for row in entries:
            print(row.id, row.name, row.teacher_id)
    elif model == "Grade":
        entries = session.query(Grade).all()
        for row in entries:
            print(row.id, row.grade, row.date_of, row.student_id, row.discipline_id)
    session.close()


def update_entry(
    model, name, group, teacher, grade, date_of, student, discipline, new_name
):
    if model == "Teacher":
        entry = session.query(Teacher).filter(Teacher.fullname == name).scalar()
        if entry:
            entry.fullname = new_name
            print(f"Entry updated: {entry.id}, {entry.fullname}")
    elif model == "Student":
        entry = session.query(Student).filter(Student.fullname == name).scalar()
        if entry:
            if new_name:
                entry.fullname = new_name
            if group:
                new_group_id = (
                    session.query(Group.id).filter(Group.name == group).scalar()
                )
                entry.group_id = new_group_id
            print(f"Entry updated: {entry.id}, {entry.fullname}, {entry.group_id}")
    elif model == "Group":
        entry = session.query(Group).filter(Group.name == name).scalar()
        if entry:
            entry.name = new_name
            print(f"Entry updated: {entry.id}, {entry.name}")
    elif model == "Discipline":
        entry = session.query(Discipline).filter(Discipline.name == name).scalar()
        if entry:
            if new_name:
                entry.name = new_name
            if teacher:
                teacher_id = (
                    session.query(Teacher.id)
                    .filter(Teacher.fullname == teacher)
                    .scalar()
                )
                entry.teacher_id = teacher_id
            print(f"Entry updated: {entry.id}, {entry.name}, {entry.teacher_id}")
    elif model == "Grade":
        student_id = (
            session.query(Student.id).filter(Student.fullname == student).scalar()
        )
        discipline_id = (
            session.query(Discipline.id).filter(Discipline.name == discipline).scalar()
        )
        entry = (
            session.query(Grade)
            .filter(
                and_(
                    Grade.date_of == datetime.strptime(date_of, "%Y-%m-%d"),
                    Grade.student_id == student_id,
                    Grade.discipline_id == discipline_id,
                )
            )
            .scalar()
        )
        if entry:
            entry.grade = grade
        print(
            f"Entry updated: {entry.grade}, {entry.date_of}, {entry.student_id}, {entry.discipline_id}"
        )
    session.commit()
    session.close()
    return entry


def remove_entry(model, name, date_of, student, discipline):
    if model == "Teacher":
        entry = session.query(Teacher).filter(Teacher.fullname == name).delete()
    elif model == "Student":
        entry = session.query(Student).filter(Student.fullname == name).delete()
    elif model == "Group":
        entry = session.query(Group).filter(Group.name == name).delete()
    elif model == "Discipline":
        entry = session.query(Discipline).filter(Discipline.name == name).delete()
    elif model == "Grade":
        student_id = (
            session.query(Student.id).filter(Student.fullname == student).scalar()
        )
        discipline_id = (
            session.query(Discipline.id).filter(Discipline.name == discipline).scalar()
        )
        entry = (
            session.query(Grade)
            .filter(
                and_(
                    Grade.date_of == datetime.strptime(date_of, "%Y-%m-%d"),
                    Grade.student_id == student_id,
                    Grade.discipline_id == discipline_id,
                )
            )
            .delete()
        )

    session.commit()
    session.close()
    return entry
