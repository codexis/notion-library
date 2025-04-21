""" Module providing a livelib parser methods """
from bs4 import BeautifulSoup
import json
import re
from service.loader import Loader


loader = Loader()

class Mif:
    """MIF Parser class"""

    PUBLISHER_NAME = 'МИФ'
    API_URL = "https://www.mann-ivanov-ferber.ru"

    def get_book_data(self, book_link_url: str):
        """ getting book info by book_link_url """

        soup = self.get_book_page_data(book_link_url)

        data_text = soup.find('script', {
            'id': '__NEXT_DATA__'
        }).text

        data_json = json.loads(data_text)
        product_data = data_json['props']['pageProps']['storeSnapshot']['productCardStore']['product']

        title_ru = product_data['baseData']['title']
        slogan_ru = product_data['baseData']['titleInList']
        authors_ru_data = product_data['baseData']['authors']
        # category_ru = product_data['baseData']['category']['name']
        # authors_ru = [author['name'] for author in authors_ru_data]

        title_orig = product_data['dataInOriginalLanguage']['title'] if product_data['dataInOriginalLanguage'] else title_ru
        slogan_orig = product_data['dataInOriginalLanguage']['titleInList'] if product_data['dataInOriginalLanguage'] else slogan_ru
        authors_orig_data = product_data['dataInOriginalLanguage']['authors'] if product_data['dataInOriginalLanguage'] else authors_ru_data

        # Transform authors_orig from a list of dictionaries to a list of strings
        authors_orig = [author['name'] for author in authors_orig_data]

        # for item in product_data['offlineParameters']['items']:
        #     if item['type'] == 'pages':
        #         pages = item['value']

        # Parse release parameters to extract year, pages, and ISBN
        release_parameters = product_data['releaseParameters']
        parsed_release_params = self.parse_release_parameters(release_parameters)

        # Download and cache image
        image_url = self.API_URL + product_data['baseData']['cover']['large']
        image_name = loader.download_and_cache_image(image_url, title_orig)

        # div_cover = soup.find('div', {
        #     'data-fixed-menu-selector': 'COVER'
        # })
        # image_url = div_cover.find_all('img')[0].attrs['src']
        # title = div_cover.find_all('h1')[0].text
        # author = div_cover.find_all('a')[1].text

        return {
            'title': title_orig,
            'title_ru': title_ru if title_ru != title_orig else None,
            'authors': authors_orig,
            'slogan': slogan_orig,
            'slogan_ru': slogan_ru,
            'publishing_house': self.PUBLISHER_NAME,
            'year': parsed_release_params['year'],
            'pages': parsed_release_params['pages'],
            'isbn': parsed_release_params['isbn'],
            'image_name': image_name,
            'link': book_link_url,
        }

    def get_book_page_data(self, book_link_url: str):
        """getting page data by page_url"""

        # page = requests.get(book_link_url, timeout=10)
        # html = page.content.decode("utf-8")

        html = loader.get_book_page(book_link_url)

        return BeautifulSoup(html, 'html.parser')

    def parse_release_parameters(self, release_parameters: str):
        """Parse release parameters HTML to extract year, pages, and ISBN"""

        # Create a BeautifulSoup object to parse the HTML
        soup = BeautifulSoup(release_parameters, 'html.parser')

        # Initialize variables
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
                # Extract the ISBN number
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
        """check book_link_url is a mif page"""
        return book_link_url.startswith(self.API_URL)
