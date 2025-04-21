""" Module providing a livelib parser methods """
import hashlib
import os
import os.path
import requests
from lxml import html
from requests import Response


class Cache:
    """Cache pages class"""

    def get(self, url: str) -> str|None:
        """check book_link_url is a mif page"""

        url_hash = self.get_url_hash(url)
        cache_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "../cache")
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
        """save data to cache"""

        url_hash = self.get_url_hash(url)

        cache_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "../cache")
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
        return hashlib.md5(url.encode()).hexdigest()

    def get_image(self, image_name: str) -> str|None:
        """Get image from cache if it exists"""
        image_path = self.get_image_path(image_name)

        if os.path.exists(image_path):
            return image_path
        else:
            print(f'Image not found in cache: {image_path}')

        return None

    def save_image(self, image_name: str, image_content: bytes):
        """Save image to cache"""
        image_path = self.get_image_path(image_name)

        try:
            with open(image_path, 'wb') as f:
                f.write(image_content)
        except Exception as e:
            print(f'Error saving image: {e}')

    def get_image_path(self, image_name: str) -> str|None:
        """Get an image path from the cache if it exists"""
        cache_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "../cache")
        if not os.path.exists(cache_dir):
            os.makedirs(cache_dir)

        return os.path.join(cache_dir, image_name)

