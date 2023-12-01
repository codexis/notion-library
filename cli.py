""" Console Python script of the Library Project """
from service.library import Library

library = Library()

if __name__ == '__main__':
    BOOK_ID = 1003006746

    book_data = library.get_book(BOOK_ID)
    print(book_data)

    res = library.export_book(book_data)
    print(res.status_code)
    print(res.text)
