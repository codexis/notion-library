""" Library Service  """
from infrastructure.cache.cache_image import CacheImage
from lib.livelib import LiveLib
from infrastructure.external.mif_client import MifClient
from lib.notion import Notion
from lib.obsidian import Obsidian
from service.loader import Loader

cache_image = CacheImage()
loader = Loader()
livelib = LiveLib()
mif = MifClient()


class Library:
    """ Library Service class """

    def __init__(self):
        super().__init__()
        self.current_book_data = None

    def get_book(self, book_link_url: str):
        """ getting book data by book_id """

        if mif.check_page_url(book_link_url):
            html = loader.get_book_page(book_link_url)
            book_data = mif.parse_book_data_from_html(html)
        elif livelib.check_page_url(book_link_url):
            book_data = livelib.get_book_data(book_link_url)
        else:
            return None

        book_data['link'] = book_link_url

        # Download and cache image
        book_data['image_name'] = loader.download_and_cache_image(book_data['image_url'], book_data['title_orig'])

        # Store the book data for later use
        self.current_book_data = book_data

        return book_data

    def save_to_notes(self) -> str:
        """ Save book data to a Markdown file """

        obsidian = Obsidian()

        if not self.current_book_data:
            return "No book data to save"

        return obsidian.save_to_notes(
            self.current_book_data,
            cache_image.get(self.current_book_data['image_name'])
        )

    @staticmethod
    def export_book(book_data: dict):
        """ export book to the Notion """

        notion = Notion()

        return notion.create_book_edition_page(book_data)
