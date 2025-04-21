"""
Client for parsing book information from the Mann-Ivanov-Ferber (МИФ) publishing house website.

This module extracts structured book data from MIF website HTML pages, including titles,
authors, publication details, and cover images in both original and Russian languages.

Classes:
    MifClient: Handles parsing operations and data extraction from the website.
"""
import json
import re
from bs4 import BeautifulSoup


class MifClient:
    """Client for parsing book information from the Mann-Ivanov-Ferber (МИФ) website.

    Attributes:
        PUBLISHER_NAME (str): Publisher's name ('МИФ').
        API_URL (str): Base URL for validation and image URL construction.
    """

    PUBLISHER_NAME = 'МИФ'
    API_URL = "https://www.mann-ivanov-ferber.ru"

    def parse_book_data_from_html(self, html: str) -> dict:
        """Extract structured book information from MIF page HTML.

        Args:
            html (str): HTML content of a MIF book page.

        Returns:
            dict: Book information with keys:
                - title: Original language title
                - title_ru: Russian title (None if same as original)
                - authors: List of author names
                - slogan: Original language subtitle
                - slogan_ru: Russian subtitle
                - publishing_house: Publisher name ('МИФ')
                - year: Publication year
                - pages: Page count
                - isbn: ISBN number
                - image_url: Cover image URL
        """

        soup = BeautifulSoup(html, 'html.parser')

        data_text = soup.find('script', {
            'id': '__NEXT_DATA__'
        }).text

        data_json = json.loads(data_text)
        product = data_json['props']['pageProps']['storeSnapshot']['productCardStore']['product']

        title_ru = product['baseData']['title']
        slogan_ru = product['baseData']['titleInList']
        authors_ru_data = product['baseData']['authors']

        if product['dataInOriginalLanguage']:
            title = product['dataInOriginalLanguage']['title']
            slogan = product['dataInOriginalLanguage']['titleInList']
            authors_data = product['dataInOriginalLanguage']['authors']
        else:
            title = title_ru
            slogan = slogan_ru
            authors_data = authors_ru_data

        authors = [author['name'] for author in authors_data]

        # Parse release parameters to extract year, pages, and ISBN
        release_parameters = product['releaseParameters']
        parsed_release_params = self.parse_release_parameters(release_parameters)

        image_url = self.API_URL + product['baseData']['cover']['large']

        # category_ru = product['baseData']['category']['name']
        # authors_ru = [author['name'] for author in authors_ru_data]

        # for item in product['offlineParameters']['items']:
        #     if item['type'] == 'pages':
        #         pages = item['value']

        # div_cover = soup.find('div', {
        #     'data-fixed-menu-selector': 'COVER'
        # })
        # image_url = div_cover.find_all('img')[0].attrs['src']
        # title = div_cover.find_all('h1')[0].text
        # author = div_cover.find_all('a')[1].text

        return {
            'title': title,
            'title_ru': title_ru if title_ru != title else None,
            'authors': authors,
            'slogan': slogan,
            'slogan_ru': slogan_ru,
            'publishing_house': self.PUBLISHER_NAME,
            'year': parsed_release_params['year'],
            'pages': parsed_release_params['pages'],
            'isbn': parsed_release_params['isbn'],
            'image_url': image_url,
        }

    def parse_release_parameters(self, release_parameters: str) -> dict:
        """Extract publication details from book release HTML.

        Args:
            release_parameters (str): HTML with book release information.

        Returns:
            dict: Publication details with keys:
                - year: Publication year
                - pages: Page count
                - isbn: ISBN number
        """

        soup = BeautifulSoup(release_parameters, 'html.parser')

        year = None
        pages = None
        isbn = None

        # Process each paragraph
        for p in soup.find_all('p'):
            text = p.get_text()

            # Extract year from publication date
            if 'Дата выхода' in text:
                # Find the year in the text (4 consecutive digits)
                year_match = re.search(r'(\d{4})', text)
                if year_match:
                    try:
                        year = int(year_match.group(1))
                    except ValueError:
                        pass

            # Extract ISBN
            elif 'ISBN' in text:
                # Extract the ISBN
                isbn_match = re.search(r'ISBN\s+([\d-]+)', text)
                if isbn_match:
                    isbn = isbn_match.group(1)

            # Extract number of pages
            elif 'Объем' in text and 'стр' in text:
                # Extract the number of pages
                pages_match = re.search(r'(\d+)\s+стр', text)
                if pages_match:
                    try:
                        pages = int(pages_match.group(1))
                    except ValueError:
                        pass

        return {
            'year': year,
            'pages': pages,
            'isbn': isbn
        }

    def check_page_url(self, book_link_url: str) -> bool:
        """Verify if the URL belongs to the MIF website.

        Args:
            book_link_url (str): URL to check.

        Returns:
            bool: True if the URL is from the MIF website, False otherwise.
        """
        return book_link_url.startswith(self.API_URL)
