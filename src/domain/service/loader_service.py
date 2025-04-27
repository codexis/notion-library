"""
Module for loading and caching web content such as pages and images.

This module provides a service layer for downloading and caching web pages and images.
It coordinates between the loader client and cache components to efficiently manage
web content retrieval and storage.

Classes:
    LoaderService: Handles web content loading and caching operations.
"""
import os
from src.infrastructure.cache.cache_page import CachePage
from src.infrastructure.cache.cache_image import CacheImage
from src.infrastructure.external.loader_client import LoaderClient

cache_page = CachePage()
cache_image = CacheImage()
loader_client = LoaderClient()

class LoaderService:
    """Service for loading and caching web content like pages and images."""

    def get_book_page(self, page_url: str, validation):
        """Retrieves HTML content from the cache or downloads it if not cached.

        Args:
            page_url: URL of the page to retrieve
            validation: Function to validate the downloaded content

        Returns:
            HTML content as string or None if retrieval fails
        """
        html = cache_page.get(page_url)
        if html is not None:
            print('From cache!')
            return html

        html = loader_client.download_page(page_url)
        if html and (validation is None or validation(page_url, html)):
            cache_page.save(page_url, html)
            return html

        print(f"Failed to retrieve or validate page content for URL: {page_url}")
        return None

    def download_and_cache_image(self, image_url: str, title_clean: str) -> str:
        """Downloads and caches an image, using the title for filename generation.

        Args:
            image_url: URL of the image to download
            title_clean: Clean title to use as a filename

        Returns:
            Name of the cached image file
        """
        ext = self._get_image_extension(image_url)
        image_name = f"{title_clean}{ext}"

        # Check if an image already exists in the cache
        if cache_image.get(image_name) is None:
            image_content = loader_client.download_image(image_url)
            if image_content:
                cache_image.save(image_name, image_content)
        else:
            print(f'Image already in cache: {image_name}')

        return image_name

    def _get_image_extension(self, image_url: str) -> str:
        """Extracts file extension from an image URL.

        Args:
            image_url: URL of the image

        Returns:
            File extension including the dot (e.g., '.jpg')
        """
        _, ext = os.path.splitext(image_url)
        if not ext:
            ext = '.jpg'  # Default extension if none found
        return ext
