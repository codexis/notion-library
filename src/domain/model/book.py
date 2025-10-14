"""Book model module for represent a book data format."""

from dataclasses import dataclass
import re


@dataclass
class Book:
    """Class for describe book fields."""

    title: str  # Original language title
    title_ru: str | None  # Russian title (None if same as original)
    authors: list[str]  # List of author names
    slogan: str | None  # Original language subtitle
    slogan_ru: str | None  # Russian subtitle
    publishing_house: str | None  # Publisher name ('МИФ')
    year: int | None  # Publication year
    pages: int | None  # Page count
    isbn: str | None # ISBN
    image_url: str | None # Cover image URL

    link: str = ''
    title_clean: str = ''
    image_name: str = ''

    def __post_init__(self):
        """Initialize additional fields after initialization."""
        # self.clean_title = self.get_clean_title()

    def get_clean_title(self) -> str:
        """Sanitize a title for use as a filename."""

        title = self.title.replace(':', '-')  # Replace colons with hyphens
        title = re.sub(r'[^\w\d\(\)\.\-\s]', '', title) # allowed characters
        title = title.strip()

        # Remove trailing hyphen if present
        if title and title[-1] == '-':
            title = title[:-1]

        return title.strip()
