"""
Module for caching web pages.

Caches HTML content using MD5 hashed URLs as filenames.
Cache is stored in the 'cache' directory at the project root.

Classes:
    CachePage: Handles web page caching operations.
"""
import hashlib
import os
import os.path
import requests


class CachePage:
    """Class for caching and retrieving web page content."""

    def get(self, url: str) -> str|None:
        """Retrieve cached HTML content for a given URL.

        Args:
            url: The URL of the web page to retrieve from cache.

        Returns:
            The cached HTML content as a string, or None if not found.
        """

        url_hash = self.get_url_hash(url)
        cache_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "../../cache")
        file_path = os.path.join(cache_dir, f"{url_hash}.html")

        if os.path.exists(file_path):
            try:
                with open(file_path, "r", encoding="utf-8") as file:
                    html_content = file.read()
                return html_content
            except Exception as e:
                print(f"Ошибка при чтении файла: {e}")
                return None

        return None

    def save(self, url: str, html_content:str):
        """Save HTML content to cache for a given URL.

        Args:
            url: The URL of the web page to cache.
            html_content: The HTML content to save.
        """

        url_hash = self.get_url_hash(url)

        cache_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "../../cache")
        if not os.path.exists(cache_dir):
            os.makedirs(cache_dir)
        file_path = os.path.join(cache_dir, f"{url_hash}.html")

        try:
            with open(file_path, "w", encoding="utf-8") as file:
                file.write(html_content)

        except requests.RequestException as e:
            print(f"Ошибка при скачивании: {e}")

        return None

    def get_url_hash(self, url: str) -> str:
        """Generate MD5 hash for a URL.

        Args:
            url: The URL to hash.

        Returns:
            MD5 hash of the URL as a hexadecimal string.
        """
        return hashlib.md5(url.encode()).hexdigest()
