import pickle
from collections import UserDict
from datetime import datetime

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
                    raise InvalidPhoneNumber
        else:
            raise InvalidPhoneNumber

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
        self.name = Name(name)
        self.phone = []
        if phone:
            for number in phone:
                try:
                    self.phone.append(Phone(number))
                except InvalidPhoneNumber:
                    print(f"The phone number {number} is invalid, phone should be in 12-digit format")
        self.birthday = Birthday(birthday)
    
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

    def add_record(self, name, phone=None, birthday = None):
        entry = Record(name, phone, birthday)
        self.data[entry.name.value] = entry

    def find_record(self, value):
        return self.data.get(value.title())

    def delete_record(self, value):
        if self.data.get(value.title()): 
            self.data.pop(value.title()) 

    def iterator(self, n = 1):
        for page in ([f"{val}" for key,val in list(sorted(self.items()))[i:i+n]] for i in range(0, len(self.data), n)):
            yield page

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

    def find_match(self, input_info):
        result = [f"Search results for \"{input_info}\":"]
        for name, rec in self.data.items():
            phones = [p.value for p in rec.phone]
            if input_info in phones or len(list(filter(lambda phone: phone.startswith(input_info), phones))) or input_info.title() in name:
                result.append(f"{name}, {rec}")
        if len(list(result)) == 1:
            result.append("No match found.") 
        return '\n'.join(result)

    def __str__(self):
        return str(self.data) 


##EXAMPLES:
book=AddressBook()
book.add_record('Senia')
book.add_record("vasia", ["123456789012", "+38(098)444-42-45", '+38(098)1111111'], '03.05.1985')
book.add_record("aNna", ["099876543210", "+38(066)7777111"], "6.4.1999")
book.add_record("tom", ["38063 777 88 99", "38 067 655 2233", "123 123 123 123"], '01.05.2009')
book.add_record("grisha", ["+38(098)000-23-45", "666 111 222345"])
book.add_record("senya", ["111 222 333 444", "+38(050)7777111"], "3.9.1976")
rec=book.find_record("senia")
rec2=book.find_record('vasia')
rec3=book.find_record('anna')
###
for i in book.iterator(2):
    print(i)
book.save_to_file('book.bin')
data = book.load_from_file('book.bin')
print(book==data)
for i in data.iterator(2):
    print(i) 
print(book.find_match('1231')) 
print(book.find_match('sen')) 