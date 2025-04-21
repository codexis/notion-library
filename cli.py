""" Console Python script of the Library Project """
from service.library import Library

library = Library()

if __name__ == '__main__':
    BOOK_LINK_URL = 'https://www.mann-ivanov-ferber.ru/catalog/product/kak-delat-poleznye-zametki/'

    book_data = library.get_book(BOOK_LINK_URL)
    print(book_data)

    # res = library.export_book(book_data)
    # print(res.status_code)
    # print(res.text)
