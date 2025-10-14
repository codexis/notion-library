""" Module providing a livelib parser methods """
from bs4 import BeautifulSoup, Tag
from src.domain.model.book import Book


class LiveLibClient:
    """LiveLib Parser class"""

    API_URL = "https://www.livelib.ru"

    soup: BeautifulSoup

    def get_book_data(self, html: str) -> Book:
        """getting book info by book_id"""

        self.soup = BeautifulSoup(html, 'html.parser')

        return Book(
            title=self.get_title(),
            title_ru=None,
            authors=[self.get_author()],
            slogan=None,
            slogan_ru=None,
            publishing_house=self.get_publishing_house(),
            year=self.get_year(),
            pages=None,
            isbn=self.get_isbn(),
            image_url=self.get_image_url(),
        )

    def get_title(self) -> str:
        """Parse title from HTML"""
        title_tag = self.soup.find('h1', {
            'class': 'bc-header__book-title'
        })
        if isinstance(title_tag, Tag):
            return title_tag.text

        return ''

    def get_author(self) -> str:
        """Parse author from HTML"""
        author_tag = self.soup.find('a', {
            'class': 'bc-header__book-author-link'
        })
        if isinstance(author_tag, Tag):
            return author_tag.text

        return ''

    def get_publishing_house(self) -> str:
        """Parse publishing house from HTML"""
        publishing_house_tag = self.soup.find('a', {
            'class': 'bc-edition__link',
            'href': lambda href: href and "publisher" in href
        })
        if isinstance(publishing_house_tag, Tag):
            return publishing_house_tag.text

        return ''

    def get_image_url(self) -> str:
        """Parse image url from HTML"""
        image_tag = self.soup.find('img', {
            'class': 'book-cover__image',
        })
        if isinstance(image_tag, Tag):
            return image_tag.attrs['src']

        return ''

    def get_isbn(self) -> str | None:
        """Parse ISBN from HTML"""
        p_all = self.soup.findAll('p')
        for p in p_all:
            if "ISBN" in p.text:
                return p.text.split('ISBN: ')[1]

        return None

    def get_year(self) -> int | None:
        """Parse year from HTML"""
        p_all = self.soup.findAll('p')
        for p in p_all:
            if "Год издания" in p.text:
                return int(p.text.split('Год издания: ')[1])

        return None

    def check_page_url(self, book_link_url: str) -> bool:
        """Check book_link_url is a mif page"""
        return book_link_url.startswith(self.API_URL)
