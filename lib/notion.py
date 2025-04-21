""" Module providing a Notion API methods """
# @see API Documentation: https://developers.notion.com/reference/retrieve-a-database
# @see API Integrations: https://www.notion.so/my-integrations
import requests


class Notion:
    """Notion API class"""

    API_URL = "https://api.notion.com"
    API_VERSION = "2022-06-28"

    api_token = ''
    database_id = ''

    def set_config(self):
        """setting a config"""

        self.api_token = os.environ.get('NOTION_API_KEY', None)
        self.database_id = os.environ.get('NOTION_DATABASE_ID', None)

    def create_book_edition_page(self, data: dict):
        """creating a book edition"""

        return self.create_page({
            "parent": {"database_id": self.database_id},
            "cover": {
                "external": {
                    "url": data['image_url']
                }
            },
            "properties": {
                "Name": {
                    "title": [
                        {
                            "text": {
                                "content": data['title']
                            }
                        }
                    ]
                },
                "Publish year": {
                    "number": int(data['year'])
                },
                "Publishing House": {
                    "select": {
                        "name": data['publishing_house']
                    }
                },
                "ISBN": {
                    "rich_text": [
                        {
                            "type": "text",
                            "text": {
                                "content": str(data['isbn'])
                            }
                        }
                    ]
                },
                "Link": {
                    "url": data['link']
                },
            }
        })

    def create_page(self, payload: dict):
        """creating a page"""

        create_url = self.API_URL + "/v1/pages"
        return requests.post(create_url, headers=self.get_headers(), json=payload, timeout=10)

    def get_headers(self):
        """constructing headers for API-request"""

        return {
            "Authorization": "Bearer " + self.api_token,
            "Content-Type": "application/json",
            "Notion-Version": self.API_VERSION,
        }
