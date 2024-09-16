#------------------------------------------------------------------------------
# Бот-асистент повинен вміти:
#   зберігати ім'я та номер телефону на диск і виводити з диску,
#   знаходити номер телефону за ім'ям, змінювати номер, і виводити всі записи
#------------------------------------------------------------------------------
from pickle_08_bot import main
from module_08 import book
import pickle

FILENAME = 'addressbook.pkl'

def save_data(address_book, filename=FILENAME):
    with open(filename, 'wb') as f:
        pickle.dump(address_book, f)

if __name__ == '__main__':
    main()
    save_data(book)
