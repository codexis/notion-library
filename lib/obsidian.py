""" Module providing a Obsidian methods """
import os
import shutil


class Obsidian:
    """Obsidian pages class"""

    def save_to_notes(self, book_data: dict, image_path: str) -> str:
        """ Save book data to a Markdown file """

        # Get books directory from the environment variable or use default
        books_dir = os.environ.get("BOOKS_DIR")
        if not books_dir:
            books_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "books")

        if not os.path.exists(books_dir):
            # os.makedirs(books_dir)
            print('is not os.path.exists')
            print(books_dir)
            return

        # Get a template file path
        template_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "../template", "book.md")

        # Read a template file
        try:
            with open(template_path, "r", encoding="utf-8") as template_file:
                template_content = template_file.read()
        except Exception as e:
            return f"Error reading template file: {e}"

        # Replace template variables with actual values
        replacements = {
            "{{authors}}": "\n  - \"[[" + "]]\"\n  - \"[[".join(book_data.get('authors', [])) + "]]\"" if book_data.get('authors', []) else "",
            "{{aliases}}": "\n  - " + book_data.get('title_ru', '') if book_data.get('title_ru', '') else "",
            "{{year}}": str(book_data.get('year', '')),
            "{{pages}}": str(book_data.get('pages', '')),
            "{{image_name}}": book_data.get('image_name', ''),
            "{{slogan}}": book_data.get('slogan_ru', ''),
            "{{book_page_url}}": book_data.get('link', '')
        }

        for placeholder, value in replacements.items():
            template_content = template_content.replace(placeholder, value)

        # Generate filename from a book title
        title = book_data.get('title', 'unknown')
        clean_title = title.replace(':', '-').replace('/', '-').replace('\\', '-')
        filename = f"{clean_title}.md"
        file_path = os.path.join(books_dir, filename)

        # Save file
        try:
            with open(file_path, "w", encoding="utf-8") as output_file:
                output_file.write(template_content)

            # Copy image to covers directory if it exists
            if 'image_name' in book_data and book_data['image_name']:
                # Get covers directory from the environment variable or use default
                covers_dir = os.environ.get("COVERS_DIR")
                if not covers_dir:
                    covers_dir = os.path.join(books_dir, "_covers")

                if not os.path.exists(covers_dir):
                    os.makedirs(covers_dir)

                if image_path:
                    dest_path = os.path.join(covers_dir, book_data['image_name'])
                    shutil.copy2(image_path, dest_path)

            return f"Book saved to {file_path}"
        except Exception as e:
            return f"Error saving file: {e}"