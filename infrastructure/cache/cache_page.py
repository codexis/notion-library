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

    CACHE_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "../../cache")

    def get(self, url: str) -> str|None:
        """Retrieve cached HTML content for a given URL.

        Args:
            url: The URL of the web page to retrieve from cache.

        Returns:
            The cached HTML content as a string, or None if not found.
        """
        cache_file_path = self._build_cache_file_path(url)
        if not os.path.exists(cache_file_path):
            return None

        return self._read_cache_file(cache_file_path)

    def save(self, url: str, html_content:str):
        """Save HTML content to cache for a given URL.

        Args:
            url: The URL of the web page to cache.
            html_content: The HTML content to save.
        """
        cache_file_path = self._build_cache_file_path(url)

        try:
            with open(cache_file_path, "w", encoding="utf-8") as file:
                file.write(html_content)
        except requests.RequestException as e:
            print(f"File downloading error: {e}")

    def _read_cache_file(self, file_path: str) -> str | None:
        """Read content from a cache file.

        Args:
            file_path: Path to the cache file.

        Returns:
            File content as string or None if reading fails.
        """
        try:
            with open(file_path, "r", encoding="utf-8") as file:
                return file.read()
        except (OSError, UnicodeDecodeError) as e:
            print(f"Failed to read cache file {file_path}: {e}")
            return None

    def _build_cache_file_path(self, url: str) -> str:
        """Build the full path to the cache file for a given URL.

        Args:
            url: The URL to build a cache path for.

        Returns:
            Full path to the cache file.
        """
        if not os.path.exists(self.CACHE_DIR):
            os.makedirs(self.CACHE_DIR)

        url_hash = self._get_url_hash(url)
        return os.path.join(self.CACHE_DIR, f"{url_hash}.html")

    def _get_url_hash(self, url: str) -> str:
        """Generate MD5 hash for a URL.

        Args:
            url: The URL to hash.

        Returns:
            MD5 hash of the URL as a hexadecimal string.
        """
        return hashlib.md5(url.encode()).hexdigest()
