import argparse
import sys

from faker import Faker
from sqlalchemy.exc import SQLAlchemyError

from database.db import session
from database.CRUD import create_entry, get_entries, update_entry, remove_entry


parser = argparse.ArgumentParser(description="CRUD for database")
parser.add_argument(
    "-a", "--action", required=True, help="Command: create, list, update, remove"
)
parser.add_argument("-m", "--model", required=True)
parser.add_argument("-n", "--name")
parser.add_argument("--group")
parser.add_argument("--teacher")
parser.add_argument("--grade")
parser.add_argument("--date_of")
parser.add_argument("--student")
parser.add_argument("--discipline")
parser.add_argument("--new_name")

arguments = parser.parse_args()
my_arg = vars(arguments)

action = my_arg.get("action")
name = my_arg.get("name")
model = my_arg.get("model")
group = my_arg.get("group")
teacher = my_arg.get("teacher")
grade = my_arg.get("grade")
date_of = my_arg.get("date_of")
student = my_arg.get("student")
discipline = my_arg.get("discipline")
new_name = my_arg.get("new_name")


fake = Faker("uk-UA")
if not name:
    name = fake.name()


def main():
    match action:
        case "create":
            create_entry(
                model, name, group, teacher, grade, date_of, student, discipline
            )
        case "list":
            get_entries(model)
        case "update":
            updated = update_entry(
                model,
                name,
                group,
                teacher,
                grade,
                date_of,
                student,
                discipline,
                new_name,
            )
            if updated:
                pass
            else:
                print("Not found: 404")
        case "remove":
            removed = remove_entry(
                model, name, group, teacher, grade, date_of, student, discipline
            )
            if removed:
                print("Entry deleted")
            else:
                print("Not found: 404")


if __name__ == "__main__":
    try:
        main()
    except SQLAlchemyError as error:
        print(error)
