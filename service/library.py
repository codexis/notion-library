""" Library Service  """
from configparser import ConfigParser
from lib.livelib import LiveLib
from lib.mif import Mif
from lib.notion import Notion
from lib.obsidian import Obsidian
from service.cache import Cache

config_object = ConfigParser()
config_object.read("config/config.ini")

cache = Cache()
livelib = LiveLib()
mif = Mif()


class Library:
    """ Library Service class """

    def __init__(self):
        super().__init__()
        self.current_book_data = None

    def get_book(self, book_link_url: str):
        """ getting book data by book_id """

        if mif.check_page_url(book_link_url):
            book_data = mif.get_book_data(book_link_url)
        elif livelib.check_page_url(book_link_url):
            book_data = livelib.get_book_data(book_link_url)
        else:
            return None

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
            cache.get_image(self.current_book_data['image_name'])
        )

    @staticmethod
    def export_book(book_data: dict):
        """ export book to the Notion """

        notion = Notion()
        notion.set_config()

        return notion.create_book_edition_page(book_data)
