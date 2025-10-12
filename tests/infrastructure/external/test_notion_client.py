import unittest
from src.infrastructure.external.notion_client import NotionClient

class TestNotionClient(unittest.TestCase):

    def setUp(self):
        self.notion_client = NotionClient('api_key_str', 'database_id_str')

    def test_format_data(self):
        data_input = {
            "image_url": "image_url_str",
            "title": "title_str",
            "link": "link_str",
            "year": 1970,
            "publishing_house": "publishing_house_str",
            "isbn": "isbn_str",
        }
        data_expected =  {
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
        self.assertEqual(self.notion_client.format_data(data_input), data_expected)

        pass
