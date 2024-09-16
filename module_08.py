#------------------------------------------------------------------------------
# Використовується як модуль для файла pickle_08_bot.py
#------------------------------------------------------------------------------
from collections import UserDict
from datetime import datetime, timedelta
import pickle

FILENAME = 'addressbook.pkl'

class Field:
    def __init__(self, value):
        self.value = value
    def __str__(self):
        return str(self.value)

class Name(Field):
    def __init__(self, value):
        super().__init__(value)

class Phone(Field):
    def __init__(self, value):
        if len(value) == 10 and value.isdigit():
            super().__init__(value)
        else:
            raise ValueError('The number format is incorrect')

class Birthday(Field):
    def __init__(self, value):
        try:
            birth_checking = datetime.strptime(value, '%d.%m.%Y')
            day_of_birth = birth_checking.strftime('%d.%m.%Y')
            super().__init__(day_of_birth)
        except ValueError:
            raise ValueError('Invalid date format. Use DD.MM.YYYY')

class Record:
    def __init__(self, name):
        self.name = Name(name)
        self.phones = []
        self.birthday = None
    def __str__(self):
        return f"Contact name: {self.name.value}, "\
                f"phones: {'; '.join(str(p) for p in self.phones)}"
    def add_phone(self, phone):
        self.phones.append(Phone(phone))
    def edit_phone(self, old_phone, new_phone):
        line = [str(p) for p in self.phones]
        index = line.index(old_phone)
        self.phones[index] = Phone(new_phone)
    def find_phone(self, phone):
        line = [str(p) for p in self.phones]
        return self.phones[line.index(phone)] if phone in line else None
    def remove_phone(self, phone):
        line = [str(p) for p in self.phones]
        if phone in line:
            index = line.index(phone)
            self.phones.pop(index)
    def add_birthday(self, day_of_birth):
        self.birthday = Birthday(day_of_birth)

class AddressBook(UserDict):
    def __str__(self):
        strg = '\n--------------- Address Book -------------------\n'
        for key, value in self.items():
            line = ', '.join(str(phone) for phone in value.phones)
            strg += f'{key}: {line} \n'
        return strg
    def add_record(self, record: Record):
        self.data[record.name.value] = record
    def find(self, name):
        if not name in self.keys():
            return None
        return self.data[name]
    def delete(self, name):
        if not name in self.keys():
            return
        del self[name]
    def get_upcoming_birthdays(self):
        current = datetime.now()
        upcoming_birthdays = []
        for name, val in self.items():
            if val.birthday is None:
                continue
            birth = datetime.strptime(val.birthday.value, '%d.%m.%Y')
            birthdate = datetime(current.year, birth.month, birth.day)
            if birthdate.toordinal() - current.toordinal() < 0:
                birthdate = datetime(current.year + 1, birth.month, birth.day)
            if birthdate.toordinal() - current.toordinal() < 7:
                date_congrats = birthdate
                if date_congrats.weekday() == 5:
                    date_congrats += timedelta(days=2)
                if date_congrats.weekday() == 6:
                    date_congrats += timedelta(days=1)
                upcoming_birthdays.append({'name': name,
                    'birthday': date_congrats.strftime('%d.%m.%Y')})
        return upcoming_birthdays

def load_data(filename=FILENAME):
    try:
        with open(filename, 'rb') as f:
            return pickle.load(f)
    except FileNotFoundError:
        return AddressBook()

book = load_data()
