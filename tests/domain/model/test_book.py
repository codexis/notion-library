"""Test cases for the BookModel class."""

import unittest
from src.domain.model.book import Book

class TestBookModel(unittest.TestCase):
    """Test cases for the LibraryService class."""

    def test_get_clean_title(self):
        """Test the get_clean_title method."""
        # Test cases
        test_cases = [
            ("Normal Title", "Normal Title"),
            ("Title with colon: subtitle", "Title with colon- subtitle"),
            ("Title with trailing dash-", "Title with trailing dash"),
            ("Title: with colon and trailing-", "Title- with colon and trailing"),
            ("Title with special chars: @#$%^&*()-", "Title with special chars- ()"),
            ("-", ""),  # Edge case: just a hyphen
            ("", ""),  # Edge case: empty string
        ]

        for input_title, expected_output in test_cases:
            result = self.get_book(input_title).get_clean_title()
            self.assertEqual(result, expected_output)

    def get_book(self, title: str) -> Book:
        """Retrieve book data from supported online sources."""
        return Book(
            title = title,
            title_ru = None,
            authors = ['Author'],
            slogan = None,
            slogan_ru = None,
            year = None,
            pages = None,
            publishing_house = None,
            isbn = None,
            image_url = None,
        )
