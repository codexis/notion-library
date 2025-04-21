""" Module providing a livelib parser methods """
import os
import re
import hashlib
import requests
from bs4 import BeautifulSoup
from infrastructure.cache.cache_page import CachePage
from infrastructure.cache.cache_image import CacheImage


cache_page = CachePage()
cache_image = CacheImage()

class Loader:
    """Loader pages class"""

    def get_book_page(self, page_url: str):
        """getting a page data by book_id"""
        html = cache_page.get(page_url)
        if html is None:
            print('Downloading page')
            page = requests.get(page_url, timeout=10)
            html = page.content.decode("utf-8")

            if self.validate(page_url, html):
                cache_page.save(page_url, html)

        else:
            print('From cache!')

        return html


    def get_page_hash(self, book_link_url: str) -> str:
        hash_object = hashlib.md5(book_link_url.encode())
        return hash_object.hexdigest()

    def validate(self, book_link_url: str, html_content: str) -> bool:
        if self.check_page_url_mif(book_link_url):
            soup = BeautifulSoup(html_content, 'html.parser')
            divs = soup.find('div', {
                'data-fixed-menu-selector': 'COVER'
            }).findAll('div')

            return divs is not None

        return True

    def check_page_url_mif(self, book_link_url: str) -> bool:
        """check book_link_url is a mif page"""
        mif_url = "https://www.mann-ivanov-ferber.ru/"
        return book_link_url.startswith(mif_url)

    def download_image(self, image_url: str) -> bytes|None:
        """Download image from URL"""
        try:
            response = requests.get(image_url, timeout=10)
            if response.status_code == 200:
                return response.content
            else:
                print(f'Failed to download image: {response.status_code}')
                return None
        except Exception as e:
            print(f'Error downloading image: {e}')
            return None

    def get_image_extension(self, image_url: str) -> str:
        """Get file extension from URL"""
        _, ext = os.path.splitext(image_url)
        if not ext:
            ext = '.jpg'  # Default extension if none found
        return ext

    def download_and_cache_image(self, image_url: str, title_orig: str) -> str:
        """Download and cache image, return image filename"""
        # Clean title for filename
        clean_title = self.clean_title_for_filename(title_orig)

        # Get file extension from URL
        ext = self.get_image_extension(image_url)

        # Create image filename
        image_name = f"{clean_title}{ext}"

        # Check if an image already exists in the cache
        if cache_image.get(image_name) is None:
            print(f'Downloading image: {image_name}')
            image_content = self.download_image(image_url)
            if image_content:
                cache_image.save(image_name, image_content)
        else:
            print(f'Image already in cache: {image_name}')

        return image_name

    def clean_title_for_filename(self, title: str) -> str:
        """Clean title to use as a filename-only letters, numbers, brackets, and dots allowed.
        Replace colons with hyphens."""
        # Replace colons with hyphens
        title = title.replace(':', '-')
        # Keep only allowed characters
        return re.sub(r'[^\w\d\(\)\.\-\s]', '', title)
