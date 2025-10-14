"""
Library service module for managing book data from different sources.

This module provides functionality for retrieving book information from various
online sources, caching book images, and exporting book data to different
note-taking applications.

Classes:
    LibraryService: Core service for book data retrieval and management.
"""
import os
from requests import Response
from src.domain.model.book import Book
from src.domain.service.loader_service import LoaderService
from src.infrastructure.cache.cache_image import CacheImage
from src.infrastructure.external.livelib_client import LiveLibClient
from src.infrastructure.external.mif_client import MifClient
from src.infrastructure.external.notion_client import NotionClient
from src.infrastructure.external.obsidian_client import ObsidianClient

cache_image = CacheImage()
loader_service = LoaderService()
livelib = LiveLibClient()
mif = MifClient()


class LibraryService:
    """Core service for retrieving, storing, and exporting book data."""

    def __init__(self):
        """Initialize the library service with empty book data."""
        super().__init__()
        self.current_book = None

    def get_book(self, book_link_url: str) -> Book | None:
        """Retrieve book data from supported online sources.

        Args:
            book_link_url (str): URL of the book page

        Returns:
            dict: Book data including title, author, and image information,
                  or None if URL is not supported
        """

        if mif.check_page_url(book_link_url):
            html = loader_service.get_book_page(book_link_url, mif.validate)
            book = mif.parse_book_data_from_html(html)

        elif livelib.check_page_url(book_link_url):
            html = loader_service.get_book_page(book_link_url, None)
            book = livelib.get_book_data(html)

        # Add Google Books APIs
        # https://developers.google.com/books/docs/v1/using?hl=ru

        else:
            return None

        if book is None:
            return None

        book.link = book_link_url
        book.title_clean = book.get_clean_title()

        # Download and cache image
        book.image_name = loader_service.download_and_cache_image(
            str(book.image_url),
            book.title_clean
        )

        # Store the book data for later use
        self.current_book = book

        return book

    def save_to_notes(self) -> str:
        """Save current book data to a Markdown file using Obsidian.

        Returns:
            str: Path to the saved file or error message
        """

        if not self.current_book:
            return "No book data to save"

        obsidian = ObsidianClient()

        return obsidian.save_to_notes(
            self.current_book,
            cache_image.get(self.current_book.image_name)
        )

    @staticmethod
    def export_book(book: Book) -> Response:
        """Export book data to a Notion database.

        Returns:
            str: URL of the created Notion page
        """

        notion = NotionClient(
            os.environ.get('NOTION_API_KEY', None),
            os.environ.get('NOTION_DATABASE_ID', None)
        )

        return notion.create_book_edition_page(book)
