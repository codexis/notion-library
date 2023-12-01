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
    """ Library Service class """

    @staticmethod
    def get_book(book_id: int):
        """ getting book data by book_id """
        return livelib.get_book_data(book_id)

    @staticmethod
    def export_book(book_data: dict):
        """ export book to notion """
        return notion.create_book_edition_page(book_data)
