""" Console Python script of the Library Project """
from src.domain.service.library_service import LibraryService

library = LibraryService()

if __name__ == '__main__':
    BOOK_LINK_URL = 'https://www.mann-ivanov-ferber.ru/catalog/product/kak-delat-poleznye-zametki/'

    book = library.get_book(BOOK_LINK_URL)
    print(book)

    # res = library.export_book(book_data)
    # print(res.status_code)
    # print(res.text)
