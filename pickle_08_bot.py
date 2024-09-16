#------------------------------------------------------------------------------
# Використовується як модуль для файла main.py
#------------------------------------------------------------------------------
from module_08 import book, Record

def input_error(func):
    def inner(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except ValueError:
            return 'Give me the name and phone please.'
        except KeyError:
            return 'There\'s no such name in the list.'
        except IndexError:
            return 'Give the name please.'
    return inner

@input_error
def parse_input(user_input):
    cmd, *args = user_input.split()
    cmd = cmd.strip().lower()
    return cmd, *args

@input_error
def add_contact(args, contacts):
    name, phone, *_ = args
    record = contacts.find(name)
    if record is None:
        new_record = Record(name)
        new_record.add_phone(phone)
        book.add_record(new_record)
        return 'The contact is added'
    if record.find_phone(phone) is None:
        record.add_phone(phone)
        return 'The contact is updated.'
    return 'The contact has this number already.'

@input_error
def change_contact(args, contacts):
    name, old_phone, new_phone = args
    record = contacts.find(name)
    if record is None:
        return 'The contact is not found.'
    if record.find_phone(old_phone) is None:
        return 'The contact doesn\'t have such number.'
    if record.find_phone(new_phone) is not None:
        record.remove_phone(old_phone)
        return 'The contact is changed.'
    record.edit_phone(old_phone, new_phone)
    return 'The contact is changed.'

@input_error
def get_number(args, contacts):
    return contacts.find(args[0])

@input_error
def add_birthday(args, contacts):
    name, birth = args
    record = contacts.find(name)
    if record is None:
        return 'The contact is not found.'
    record.add_birthday(birth)
    return 'The birthday is added'

@input_error
def show_birthday(name, contacts):
    record = contacts.find(name[0])
    if record is None:
        return 'The contact is not found.'
    return record.birthday

def main():
    print('Welcome to the assistant bot!')
    while True:
        user_input = input('Enter a command: ')
        command, *args = parse_input(user_input)
        if command in ['close', 'exit']:
            print('Good bye!')
            break
        elif command == 'hello':
            print('How can I help you?')
        elif command == 'add':
            print(add_contact(args, book))
        elif command == 'change':
            print(change_contact(args, book))
        elif command == 'phone':
            print(get_number(args, book))
        elif command == 'all':
            print(book)
        elif command == 'add-birthday':
            print(add_birthday(args, book))
        elif command == 'show-birthday':
            print(show_birthday(args, book))
        elif command == 'birthdays':
            print('------- Upcoming birthday events -------')
            for event in book.get_upcoming_birthdays():
                print(f"{event['name']}: {event['birthday']}")
        else:
            print('Invalid command.')


