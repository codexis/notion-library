"""Test cases for the NotionClient class."""

import unittest
from src.domain.model.book import Book
from src.infrastructure.external.notion_client import NotionClient

class TestNotionClient(unittest.TestCase):
    """Test cases for the NotionClient class."""

    def setUp(self):
        """Set up the test environment."""
        self.notion_client = NotionClient('api_key_str', 'database_id_str')

    def test_format_data(self):
        """Test the format_data method."""

        book = Book(
            title = "title_str",
            title_ru = None,
            authors = ['Author Name'],
            slogan = None,
            slogan_ru = None,
            link = "link_str",
            year = 1970,
            pages = None,
            publishing_house = "publishing_house_str",
            isbn = "isbn_str",
            image_url = "image_url_str",
        )
        data_expected = {
            'cover': {'external': {'url': 'image_url_str'}},
            'parent': {'database_id': 'database_id_str'},
            'properties': {
                'ISBN': {'rich_text': [{'text': {'content': 'isbn_str'}, 'type': 'text'}]},
                'Link': {'url': 'link_str'},
                'Name': {'title': [{'text': {'content': 'title_str'}}]},
                'Publish year': {'number': 1970},
                'Publishing House': {'select': {'name': 'publishing_house_str'}}
            }
        }
        self.assertEqual(self.notion_client.format_book_data(book), data_expected)
