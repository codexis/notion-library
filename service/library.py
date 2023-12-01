""" Library Service  """
from configparser import ConfigParser
from lib.livelib import LiveLib
from lib.notion import Notion

config_object = ConfigParser()
config_object.read("config/config.ini")

notion = Notion()
notion.set_config(dict(config_object["NOTION"]))

livelib = LiveLib()


class Library:
    """Library Service class"""

    def get_book(self, book_id: int):
        return livelib.get_book_data(book_id)

    def export_book(self, book_data: dict):
        return notion.create_book_edition_page(book_data)
