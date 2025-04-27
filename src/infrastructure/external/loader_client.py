"""Client for downloading web content such as pages and images with error handling.

This module provides functionality for downloading various types of web content
with proper error handling and timeout settings. It abstracts away the complexities
of making HTTP requests and handling potential errors.

Classes:
    LoaderClient: Handles web content downloading with error management.
"""
import requests
from src.domain.exception.library_exceptions import DownloadError


class LoaderClient:
    """Client for downloading web content with proper error handling."""

    def download_page(self, page_url: str) -> str|None:
        """Downloads a web page and returns its content as a string.

        Args:
            page_url: URL of the page to download

        Returns:
            String content of the downloaded page or None if download fails
        """
        print('Downloading page')
        try:
            return self._download(page_url).decode("utf-8")
        except DownloadError as e:
            print(f'Error downloading page: {e}')
            return None

    def download_image(self, image_url: str) -> bytes|None:
        """Downloads an image and returns its content as bytes.

        Args:
            image_url: URL of the image to download

        Returns:
            Bytes content of the downloaded image or None if download fails
        """
        print('Downloading image')
        try:
            return self._download(image_url)
        except DownloadError as e:
            print(f'Error downloading image: {e}')
            return None

    def _download(self, url) -> bytes:
        """Internal method that handles the actual download process.

        Args:
            url: URL to download content from

        Returns:
            Raw bytes content of the downloaded resource
        """
        try:
            response = requests.get(url, timeout=10)
        except requests.exceptions.RequestException as e:
            raise DownloadError(f'Download error: {e}') from e

        if response.status_code != 200:
            raise DownloadError(f'Download error: {response.status_code}')

        return response.content
