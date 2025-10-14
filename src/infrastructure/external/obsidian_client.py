""" 
Module for interacting with an Obsidian notes system.

This module provides functionality to save book data as Markdown files in Obsidian format,
including handling book metadata and cover images.

Classes:
    ObsidianClient: Client for creating and managing book notes in Obsidian format
"""
import os
import shutil
from src.domain.exception.library_exceptions import DirNotExists
from src.domain.model.book import Book


class ObsidianClient: # pylint: disable=too-few-public-methods
    """Client for creating and managing book notes in Obsidian format."""

    BOOKS_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "../storage/books")
    COVERS_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "../storage/covers")
    BOOK_TEMPLATE_FILE_PATH = os.path.join(
        os.path.dirname(os.path.abspath(__file__)),
        "../template",
        "book.md"
    )

    def save_to_notes(self, book: Book, image_path: str | None) -> str:
        """Saves book data to an Obsidian-formatted Markdown file and copies the cover image.

        Args:
            book: Dictionary containing book metadata (title, authors, year, pages, etc.)
            image_path: Path to the book cover image file

        Returns:
            String message indicating success or error details
        """

        template_content = ''

        # Read a template file
        try:
            with open(self.BOOK_TEMPLATE_FILE_PATH, "r", encoding="utf-8") as template_file:
                template_content = template_file.read()
        except (OSError, UnicodeDecodeError) as e:
            return f"Error reading template file: {e}"

        # Replace template variables with actual values
        replacements = {
            "{{authors}}": self._build_authors(book),
            "{{aliases}}": self._build_aliases(book),
            "{{year}}": str(book.year),
            "{{pages}}": str(book.pages),
            "{{image_name}}": book.image_name,
            "{{slogan}}": book.slogan_ru,
            "{{book_page_url}}": book.link
        }

        for placeholder, value in replacements.items():
            template_content = template_content.replace(placeholder, str(value))

        try:
            book_file_path = self._build_book_file_path(book)
            cover_file_path = None
            if book.image_name:
                cover_file_path = self._build_cover_file_path(book)
        except DirNotExists as e:
            return str(e)

        try:
            # Save file
            with open(book_file_path, "w", encoding="utf-8") as output_file:
                output_file.write(template_content)

            # Copy image to covers directory if it exists
            if image_path and cover_file_path:
                shutil.copy2(image_path, cover_file_path)

            return f"Book saved to {book_file_path}"
        except OSError as e:
            return f"Error saving file: {e}"

    def _build_authors(self, book: Book) -> str:
        """Formats the list of authors in Obsidian wiki-link format.

        Returns:
            Formatted string with authors as Obsidian wiki-links or empty string if no authors
        """
        return "\n  - \"[[" + "]]\"\n  - \"[[".join(book.authors) + "]]\"" \
            if book.authors \
            else ""

    def _build_aliases(self, book: Book) -> str:
        """Formats the book's alternative title as an alias.

        Returns:
            Formatted string with the Russian title as an alias or empty string if not available
        """
        return "\n  - \"" + book.title_ru + "\"" \
            if book.title_ru \
            else ""

    def _build_book_file_path(self, book: Book) -> str:
        """Constructs the file path for the book's Markdown file.

        Returns:
            Full path to the Markdown file for the book
        """
        filename = f"{book.title_clean}.md"

        books_dir = self._get_books_dir()

        return os.path.join(books_dir, filename)

    def _get_books_dir(self) -> str:
        """Get the path to the books directory from the environment variable or default."""
        books_dir = os.environ.get("BOOKS_DIR")
        if not books_dir:
            if not os.path.exists(self.BOOKS_DIR):
                os.makedirs(self.BOOKS_DIR)
            books_dir = self.BOOKS_DIR

        if not os.path.exists(books_dir):
            raise DirNotExists(f"Books dir doesn't exists: {books_dir}")

        return books_dir

    def _build_cover_file_path(self, book: Book) -> str:
        """Constructs the file path for the book's Markdown file."""
        covers_dir = self._get_covers_dir()
        return os.path.join(covers_dir, book.image_name)

    def _get_covers_dir(self) -> str:
        """Get the path to the covers directory from the environment variable or default."""
        covers_dir = os.environ.get("COVERS_DIR")
        if not covers_dir:
            if not os.path.exists(self.COVERS_DIR):
                os.makedirs(self.COVERS_DIR)
            covers_dir = self.COVERS_DIR

        if not os.path.exists(covers_dir):
            raise DirNotExists(f"Covers dir doesn't exists: {covers_dir}")

        return covers_dir
