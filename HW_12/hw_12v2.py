from curses.ascii import isdigit
import functools
import pickle
from collections import UserDict
from datetime import datetime


def command_handler(func):
    @functools.wraps(func)
    def wrapper(*args):
        try:
            return func(*args)
        except TypeError as e:
            print('Please enter the required args')
        except ValueError as e:
            return str(e)
        except KeyError as e:
            return str(e)
        except IndexError as e:
            return str(e) 
    return wrapper

class InvalidPhoneNumber(Exception):
    pass

class Field:
    def __init__(self, value):
        self._value = None 
        self.value = value 

class Name(Field):

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, value):
        self._value = value.title()

class Phone(Field): 

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, value):
        replace_symbols = "(-)+ "
        clean_phone =  ''.join(filter(lambda symbol: symbol not in replace_symbols, value))
        if len(clean_phone) == 12:
            for s in clean_phone:
                if s.isdigit():
                    self._value = clean_phone
        else:
            print(f"The phone number {clean_phone} is invalid, phone should be in 12-digit format")

    def __str__(self):
        return f"Phone: {self.value}"

class Birthday(Field):
    
    @property
    def value(self):
        return self._value
    
    @value.setter
    def value(self, value):
        if value:
            try:
                value_parse = value.split(".")
                value = f"{int(value_parse[0]):02d}.{int(value_parse[1]):02d}.{int(value_parse[2])}"
                datetime.strptime(value, "%d.%m.%Y").date()
                self._value = value
            except (IndexError, ValueError):
                print('Wrong date format, date format should be: dd.mm.yyyy')
                self._value = None 

class Record:

    def __init__(self, name, phone = None, birthday = None):
        self.name = name
        self.phone = phone
        self.birthday = birthday
    
    def add_number(self, value):
        try:
            self.phone.append(Phone(value))
        except InvalidPhoneNumber:
            print(f"The phone number {value} is invalid")
 
    def remove_number(self, value):
        if value not in [p.value for p in self.phone]:
            print(f"The pnone number {value} not found")
        else:
            for i in self.phone:
                if i.value == value:
                    self.phone.remove(i)
            
    def edit_number (self, value, new_value): 
        if self.phone:
            if value not in [p.value for p in self.phone]:
                print (f"Old phone {value} not found")
            if new_value in [p.value for p in self.phone]:
                print (f"New phone {new_value} is already in the list")
            for n, i in enumerate(self.phone):
                if i.value == value and new_value not in [p.value for p in self.phone]:
                    try:
                        self.phone[n] = Phone(new_value)
                    except InvalidPhoneNumber:
                        print(f"The phone number {new_value} is invalid")
        else:
            print ("There is none of the numbers in the list")
    
    def days_to_birthday(self):
        if self.birthday.value:
            current_date = datetime.today().date()
            birthday = datetime.strptime(f"{self.birthday.value[:6]}{current_date.year}", "%d.%m.%Y").date()
            if birthday < current_date:
                birthday = birthday.replace(year=current_date.year+1)
            days_left = (birthday - current_date).days
            return f"{days_left}"
        return 'Date of birth not indicated' 

    def __str__(self):
        if self.birthday.value is not None:
            return f"Record of {self.name.value}, phones {[p.value for p in self.phone]}, birthday on {self.birthday.value}, birthday in {self.days_to_birthday()} day(s)"  
        return f"Record of {self.name.value}, phones {[p.value for p in self.phone]}"

class AddressBook(UserDict):

    @command_handler
    def add_record(self):
        name_arg = input("Please enter the name:\n").lower().strip()
        while not name_arg:
            name_arg = input("You must enter the name:\n").lower().strip()
        name = Name(name_arg)
        phone = []
        phone_arg = input("Please enter the phone numbers following the 'Enter' key, or skip by hitting the 'Enter':\n").lower().strip()
        while phone_arg:
            number = Phone(phone_arg)
            if number.value:
                phone.append(number)
            phone_arg = input("Please enter another phone number following the 'Enter' key, or skip by hitting the 'Enter':\n").lower().strip()
        birthday=None
        bday_arg = input("Please enter the date of birth in dd.mm.yyyy format, or skip by hitting the 'Enter':\n").lower().strip()
        birthday = Birthday(bday_arg)                   
        entry = Record(name, phone, birthday)
        self.data[entry.name.value] = entry
        print(f'The Record of {name.value} was added to the AddressBook')

    def find_record(self):
        name_find = input("Please enter the name of the Record that you are looking for:\n").lower().strip().title()
        if self.data.get(name_find):
            print(self.data.get(name_find))
        else:
            print(f'The Record {name_find.title()} not found in the AddressBook')

    def delete_record(self):
        name_del = input("Please enter the name of the Record that you want to delete or press 'Enter' to go back:\n").lower().strip()
        if self.data.get(name_del.title()): 
            self.data.pop(name_del.title())
            print(f'The Record of {name_del.title()} was removed from the AddressBook')
        else:
            print(f'The Record {name_del.title()} not found in the AddressBook')

    def iterator(self, n: int = 2):
        n_change = input(f"Currently displaying {n} item(s) per page.\nIf you want to change the # of items per page please type the # or press 'Enter' to skip: ").lower().strip()
        if n_change.isdigit():
            n = n_change
        else:
            print("Not recognized format")
        for page in ([f"{val}" for key,val in list(sorted(self.items()))[i:i+int(n)]] for i in range(0, len(self.data), int(n))):
            yield page

    def show_contacts(self, n = 2):
        for contacts in self.iterator(n):
            print(contacts)

    def save_to_file(self, filename):
        try:
            with open(filename, "wb") as file:
                pickle.dump(self.data, file)
            print(f"The file \"{filename}\" was saved successfully")
        except (FileNotFoundError, AttributeError, MemoryError):
            print(f"An error occurred while tried to save the file \"{filename}\"")

    def load_from_file(self, filename):
        try:
            with open(filename, 'rb') as file:
                self.data = pickle.load(file)
                print(f"Load from file \"{filename}\" successful")
                return self
        except (FileNotFoundError, AttributeError, MemoryError):
            print(f"An error occurred while tried to open the file \"{filename}\"")

    def find_match(self):
        input_info = input("Please enter the characters of the name or phone number to look for the closest match in the Records:\n").lower().strip()
        result = [f"Search results for \"{input_info}\":"]
        for name, rec in self.data.items():
            phones = [p.value for p in rec.phone]
            if input_info in phones or len(list(filter(lambda phone: phone.startswith(input_info), phones))) or input_info.title() in name or \
                len(list(filter(lambda name: name.startswith(input_info), name))):
                result.append(f"{rec}")
        if len(list(result)) == 1:
            result.append("No match found.") 
        print('\n'.join(result))

    def show_commands(self):
        print(commands_desc)

    def __str__(self):
        return str(self.data) 

class CommandHandler:

    def __call__(self, command):
        if command in exit_commands:
            return False
        elif command in action_commands:
            commands_func[command]()
            return True
        else:
            print("Sorry, the assistant does not recognize your command.")
        return True

book = AddressBook()
action_commands = ["help", "add_record", "find_match", "find_record", "delete_record", "show_records"]
exit_commands = ["good_bye", "close", "exit"]
commands_description = ["Returns the list of available CLI commands", "Adding the Record to the AddressBook", \
    "Looking for the match among all Records", "Searching the Record by name", \
    "Deleting the Record", "Returns all Records in the AddressBook in increments", "Exits the program"]
functions_list = [book.show_commands, book.add_record, book.find_match, book.find_record, book.delete_record, book.show_contacts, exit]
commands_func = {cmd: func for cmd, func in zip(action_commands, functions_list)}
commands_desc = [f"<<{cmd}>> - {desc}" for cmd, desc in zip(action_commands + [', '.join(exit_commands)], commands_description)]


data_file = "boot.bin"

def main():
    book.load_from_file(data_file)
    command = CommandHandler()
    input_msg = input("Hello and welcome to the personal assistant!\nTo check the full list of commands, please type 'help'.\nPlease enter the command:\n").lower().strip()
    while command(input_msg):
        input_msg = input("Please enter the command:\n").lower().strip() 
    book.save_to_file(data_file)
    print("Good bye!")

if __name__ == "__main__":
    main()