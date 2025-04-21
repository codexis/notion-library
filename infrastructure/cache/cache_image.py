""" Module providing a livelib parser methods """
import os
import os.path


class CacheImage:
    """Cache images class"""

    def get(self, image_name: str) -> str|None:
        """Get image from cache if it exists"""
        image_path = self.get_image_path(image_name)

        if os.path.exists(image_path):
            return image_path
        else:
            print(f'Image not found in cache: {image_path}')

        return None

    def save(self, image_name: str, image_content: bytes):
        """Save image to cache"""
        image_path = self.get_image_path(image_name)

        try:
            with open(image_path, 'wb') as f:
                f.write(image_content)
        except Exception as e:
            print(f'Error saving image: {e}')

    def get_image_path(self, image_name: str) -> str|None:
        """Get an image path from the cache if it exists"""
        cache_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "../../cache")
        if not os.path.exists(cache_dir):
            os.makedirs(cache_dir)

        return os.path.join(cache_dir, image_name)

