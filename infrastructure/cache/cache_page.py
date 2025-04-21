
import hashlib
import os
import os.path
import requests


class CachePage:
    """Cache pages class"""

    def get(self, url: str) -> str|None:
        """check book_link_url is a mif page"""

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
        """save data to cache"""

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
        return hashlib.md5(url.encode()).hexdigest()
