"""Module providing a livelib parser methods"""

import requests
from bs4 import BeautifulSoup


class LiveLib:
    """LiveLib Parser class"""

    API_URL = "https://www.livelib.ru"

    def get_book_data(self, book_id: int):
        """getting a book info by book_id"""

        soup = self.get_book_page_data(book_id)

        title = soup.find('h1', {
            'class': 'bc__book-title'
        }).text

        author = soup.find('a', {
            'class': 'bc-author__link'
        }).text

        publishing_house = soup.find('a', {
            'class': 'bc-edition__link',
            'href': lambda href: href and "publisher" in href
        }).text

        image_url = soup.find('div', {
            'class': 'bc-menu__image-wrapper',
        }).attrs['onclick']
        image_url = image_url.split("event, '")[1]
        image_url = image_url.split("', '")[0]

        isbn = ''
        year = ''

        p_all = soup.findAll('p')
        for p in p_all:
            if "ISBN" in p.text:
                isbn = p.text.split('ISBN: ')[1]
            elif "Год издания" in p.text:
                year = p.text.split('Год издания: ')[1]

        return {
            'title': title,
            'author': author,
            'publishing_house': publishing_house,
            'year': year,
            'isbn': isbn,
            'image_url': image_url,
            'link': self.get_book_page_url(book_id),
        }

    def get_book_page_data(self, book_id: int):
        """getting a page data by book_id"""

        page_url = self.get_book_page_url(book_id)
        page = requests.get(page_url, timeout=10)
        html = page.content.decode("utf-8")

        return BeautifulSoup(html, 'html.parser')

    def get_book_page_url(self, book_id: int):
        """construct page_url of a book by book_id"""

        return self.API_URL + "/book/" + str(book_id)
