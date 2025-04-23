""" Module providing a livelib parser methods """
from bs4 import BeautifulSoup


class LiveLibClient:
    """LiveLib Parser class"""

    API_URL = "https://www.livelib.ru"

    def get_book_data(self, html: str):
        """getting a book info by book_id"""

        soup = BeautifulSoup(html, 'html.parser')

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
        }

    def check_page_url(self, book_link_url: str) -> bool:
        """check book_link_url is a mif page"""
        return book_link_url.startswith(self.API_URL)
