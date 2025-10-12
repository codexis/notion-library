import unittest
from src.domain.service.library_service import LibraryService

class TestLibraryService(unittest.TestCase):

    def setUp(self):
        self.library_service = LibraryService()

    def test__get_clean_title(self):
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
            result = self.library_service._get_clean_title(input_title)
            self.assertEqual(result, expected_output)
