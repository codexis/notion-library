"""
Module for caching images.

Stores and retrieves images in their original format to avoid repeated downloads.
Cache is stored in the 'cache' directory at the project root.

Classes:
    CacheImage: Handles image caching operations.
"""
import os
import os.path


class CacheImage:
    """Class for caching and retrieving images."""

    CACHE_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "../storage/cache/image")

    def get(self, image_name: str) -> str|None:
        """Retrieve an image path from the cache if it exists.

        Args:
            image_name: Name of the image file to retrieve.

        Returns:
            Full path to the cached image, or None if not found.
        """
        image_path = self.get_image_path(image_name)

        if os.path.exists(image_path):
            return image_path

        print(f'Image not found in cache: {image_path}')

        return None

    def save(self, image_name: str, image_content: bytes):
        """Save image content to the cache.

        Args:
            image_name: Name of the image file to save.
            image_content: Binary content of the image.
        """
        image_path = self.get_image_path(image_name)

        try:
            with open(image_path, 'wb') as f:
                f.write(image_content)
        except OSError as e:
            print(f'Error saving image: {e}')

    def get_image_path(self, image_name: str) -> str:
        """Generate a full path for an image in the cache.

        Args:
            image_name: Name of the image file.

        Returns:
            Full path to the image in the cache directory.
        """
        if not os.path.exists(self.CACHE_DIR):
            os.makedirs(self.CACHE_DIR)

        return os.path.join(self.CACHE_DIR, image_name)
