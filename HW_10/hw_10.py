from collections import UserDict

class Field:
    def __init__(self, value):
        self.value = value

class Name(Field):

    def __init__(self, value):
        super().__init__(value)
        self.value = value.title()

class Phone(Field):
    pass

class Record:

    def __init__(self, name, phone = None):
        self.name = Name(name)
        if phone is None:
            self.phone = []
        else:
            self.phone = [Phone(_phone) for _phone in phone]
    
    def add_number(self, value):
        self.phone.append(Phone(value))


    def remove_number(self, value:str):
        for i in self.phone:
            if i.value == value:
                self.phone.remove(i)

    def edit_number (self, value, new_value):
        for n, i in enumerate(self.phone):
            if i.value == value:
                self.phone[n] = Phone(new_value)

    def __str__(self):
        return f"Record of {self.name.value}, phones {[p.value for p in self.phone]}"

class AddressBook(UserDict):

    def add_record(self, name, phone=None):
        entry = Record(name, phone)
        self.data[entry.name.value] = entry

    def find_record(self, value):
        return self.data.get(value.title())

    def delete_record(self, value):
        if self.data.get(value.title()):
            self.data.pop(value.title())

    def __str__(self):
        return str(self.data)


##EXAMPLES:
book=AddressBook()
book.add_record('Senia')
book.add_record("vasia", ["111111", "2222222"])
rec=book.find_record("senia")
rec2=book.find_record('vasia')

rec.add_number("99999")

rec.add_number('444444')

book.delete_record("senia")

rec.remove_number('99999')
rec.edit_number('444444', '666')

