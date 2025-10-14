"""
Main window module for the Library Project application.

This module provides the graphical user interface for the Library Project,
allowing users to search for books, preview their details, and export them
to various destinations like Obsidian notes.

Classes:
    App: Main application window handling core functionality.
    AppUI: User interface components and layout management.
"""
import json
import customtkinter as ctk
from dotenv import load_dotenv
from PIL import Image
from src.domain.model.book import Book
from src.infrastructure.cache.cache_image import CacheImage
from src.domain.service.library_service import LibraryService


load_dotenv()
library = LibraryService()
cache_image = CacheImage()


class App(ctk.CTk):
    """
    Main application window class for the Library Project.

    Handles core functionality including book data retrieval, 
    display formatting, and export operations.
    """

    app_title = "Books Library"

    def __init__(self):
        """Initialize the application window with default settings."""
        super().__init__()
        self.geometry("1100x1000")
        self.title(self.app_title)
        self.current_book = None

        # Use composition for UI elements
        self.ui = AppUI(self)

    def export_book(self):
        """Export book data to the external service when the export button is clicked."""
        book_link = str(self.ui.link_entry.get())

        print(f"book_link: {book_link}")
        book = library.get_book(book_link)

        status_msg = json.dumps(book, indent=2, ensure_ascii=False)
        self.ui.status_label.configure(text=status_msg)

        res = library.export_book(book)
        result_json = json.loads(res.text)
        status_msg += "\n\ncode: " + str(res.status_code)
        status_msg += "\nresult: " + json.dumps(result_json, indent=2, ensure_ascii=False)

        self.ui.status_label.configure(text=status_msg)

    def grab_data(self):
        """Retrieve and display book data when the preview button is clicked."""
        book_link = str(self.ui.link_entry.get())
        print(f"book_link: {book_link}")

        book = library.get_book(book_link)
        if book is not None:
            # Store the book data for later use
            self.current_book = book

            # Format book data as a table
            table = self.format_book_data_as_table(book)

            # Display the table
            self.ui.status_label.configure(text=table)

            # Display the book cover image if available
            if book.image_name:
                self.display_book_image(book.image_name)

            # Show the Save to Notes button
            self.ui.save_button.grid()

            print(f"Previewed book: {book.title_clean}")
        else:
            self.ui.status_label.configure(
                text="Could not retrieve book data. Please check the URL."
            )
            # Hide the Save to Notes button if no book data
            self.ui.save_button.grid_remove()

    def format_book_data_as_table(self, book: Book) -> str:
        """Format book data as a readable text table."""
        table = f"Book Information:\n{'=' * 50}\n"

        # Add title
        if book.title != '':
            table += f"Title: {book.title}\n"
        if book.title_clean != '':
            table += f"Title (clean): {book.title_clean}\n"

        # Add authors
        if book.authors:
            authors = ", ".join(book.authors) \
                if isinstance(book.authors, list) \
                else book.authors
            table += f"Author(s): {authors}\n"

        # Add a publishing house
        if book.publishing_house:
            table += f"Publisher: {book.publishing_house}\n"

        # Add year
        if book.year:
            table += f"Year: {book.year}\n"

        # Add pages
        if book.pages:
            table += f"Pages: {book.pages}\n"

        # Add ISBN
        if book.isbn:
            table += f"ISBN: {book.isbn}\n"

        # Add a link
        if book.link:
            table += f"Link: {book.link}\n"

        return table

    def display_book_image(self, image_name):
        """Display book cover image in the UI.

        Args:
            image_name (str): Name of the image file to display
        """
        image_path = cache_image.get(image_name)

        print(f'image_path: {image_path}')

        if image_path:
            try:
                # Load the image
                img = Image.open(image_path)

                # Resize the image to fit in the UI
                max_width = 300
                max_height = 400
                img.thumbnail((max_width, max_height))

                # Convert to CTkImage
                photo = ctk.CTkImage(img, size=(max_width, max_height))

                if self.ui.image_label is not None:
                    self.ui.image_label.configure(image=photo)
                else:
                    self.ui.image_label = ctk.CTkLabel(master=self, text="", image=photo)
                    self.ui.image_label.grid(
                        row=3,
                        column=0,
                        columnspan=4,
                        sticky="nsew",
                        padx=20,
                        pady=20
                    )
                self.ui.image_label.image = photo
            except OSError as e:
                print(f"OS error when handling image file: {e}")
            except ValueError as e:
                print(f"Invalid parameter or operation in image processing: {e}")

    def save_to_notes(self):
        """Save current book data to Obsidian notes."""
        result_message = library.save_to_notes()

        self.ui.status_label.configure(text=result_message)
        print(result_message)


class AppUI: # pylint: disable=too-few-public-methods
    """User interface component class for the Library application.

    Manages UI elements, their layout, and visual presentation.
    """

    def __init__(self, master):
        """Initialize UI components and attach them to the master window.

        Args:
            master (App): Parent application window
        """
        self.top_label = ctk.CTkLabel(master=master, width=200, height=100, text=master.app_title)
        self.link_label = ctk.CTkLabel(master=master, width=150, text="Link to export")
        self.status_label = ctk.CTkLabel(master=master, width=550, text="", justify="left")
        self.image_label = None

        self.link_entry = ctk.CTkEntry(master=master, width=700)

        self.grab_button = ctk.CTkButton(master, command=master.grab_data, text="Preview")
        self.save_button = ctk.CTkButton(master, command=master.save_to_notes, text="Save to Notes")

        # Setup UI elements
        self.setup_ui()

    def setup_ui(self):
        """Configure UI elements layout and initial state."""
        self.top_label.grid(row=0, column=1, sticky="nsew")
        self.link_label.grid(row=1, column=0, sticky="nsew")
        self.status_label.grid(row=2, column=0, columnspan=4, sticky="nsew", padx=20, pady=20)

        self.link_entry.insert("0", "Enter link to export here...")
        self.link_entry.grid(row=1, column=1, sticky="nsew")

        self.grab_button.grid(row=1, column=3, padx=20, pady=10)
        self.save_button.grid(row=4, column=0, columnspan=4, sticky="nsew", padx=20, pady=10)
        self.save_button.grid_remove()  # Hide the button initially


if __name__ == '__main__':
    app = App()
    app.mainloop()
