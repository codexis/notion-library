""" Module providing Notion API methods """
# @see API Documentation: https://developers.notion.com/reference/retrieve-a-database
# @see API Integrations: https://www.notion.so/my-integrations

import requests
from src.domain.model.book import Book


class NotionClient:
    """Notion API class"""

    API_URL = "https://api.notion.com"
    API_VERSION = "2022-06-28"

    def __init__(self, api_token, database_id):
        super().__init__()
        self.api_token = api_token
        self.database_id = database_id

    def create_book_edition_page(self, book: Book):
        """Create a book edition"""

        return self.create_page(self.format_book_data(book))

    def format_book_data(self, book: Book) -> dict:
        """Format book data for API request"""

        return {
            "parent": {"database_id": self.database_id},
            "cover": {
                "external": {
                    "url": book.image_url
                }
            },
            "properties": {
                "Name": {
                    "title": [
                        {
                            "text": {
                                "content": book.title
                            }
                        }
                    ]
                },
                "Publish year": {
                    "number": book.year
                },
                "Publishing House": {
                    "select": {
                        "name": book.publishing_house
                    }
                },
                "ISBN": {
                    "rich_text": [
                        {
                            "type": "text",
                            "text": {
                                "content": book.isbn
                            }
                        }
                    ]
                },
                "Link": {
                    "url": book.link
                },
            }
        }

    def create_page(self, payload: dict):
        """Create a page"""

        create_url = self.API_URL + "/v1/pages"
        return requests.post(create_url, headers=self.get_headers(), json=payload, timeout=10)

    def get_headers(self):
        """Construct headers for API request"""

        return {
            "Authorization": "Bearer " + self.api_token,
            "Content-Type": "application/json",
            "Notion-Version": self.API_VERSION,
        }
