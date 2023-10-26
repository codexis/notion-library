""" This is a main Python script of the Library Project """
from configparser import ConfigParser
from lib.livelib import LiveLib
from lib.notion import Notion

config_object = ConfigParser()
config_object.read("config/config.ini")

notion = Notion()
notion.set_config(dict(config_object["NOTION"]))

livelib = LiveLib()

if __name__ == '__main__':
    BOOK_ID = 1003006746

    book_data = livelib.get_book_data(BOOK_ID)
    print(book_data)

    res = notion.create_book_edition_page(book_data)
    print(res.status_code)
    print(res.text)
