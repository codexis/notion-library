""" Main window Python script of the Library Project """
import json
import customtkinter as ctk
from dotenv import load_dotenv
from PIL import Image, ImageTk
from src.infrastructure.cache.cache_image import CacheImage
from src.domain.service.library_service import LibraryService


load_dotenv()
library = LibraryService()
cache_image = CacheImage()

class App(ctk.CTk):
    """ App Window Main class """

    app_title = "Books Library"

    def __init__(self):
        super().__init__()
        # self.image_label = None
        self.geometry("1100x1000")
        self.title(self.app_title)
        self.current_book_data = None

        self.top_label = ctk.CTkLabel(master=self, width=200, height=100, text=self.app_title)
        self.top_label.grid(row=0, column=1, sticky="nsew")

        self.link_label = ctk.CTkLabel(master=self, width=150, text="Link to export")
        self.link_label.grid(row=1, column=0, sticky="nsew")

        self.link_entry = ctk.CTkEntry(master=self, width=700)
        # self.link_entry.insert("0", "https://www.mann-ivanov-ferber.ru/catalog/product/kak-delat-poleznye-zametki/")
        self.link_entry.insert("0", "https://www.livelib.ru/book/1000455527-kak-rabotat-po-4-chasa-v-nedelyu-i-pri-etom-ne-torchat-v-ofise-ot-zvonka-do-zvonka-zhit-gde-ugodno-i-bogatet-timoti-ferris")
        self.link_entry.grid(row=1, column=1, sticky="nsew")

        self.grab_button = ctk.CTkButton(self, command=self.grab_data, text="Preview")
        self.grab_button.grid(row=1, column=3, padx=20, pady=10)

        self.status_label = ctk.CTkLabel(master=self, width=550, text="", justify="left")
        self.status_label.grid(row=2, column=0, columnspan=4, sticky="nsew", padx=20, pady=20)

        self.save_button = ctk.CTkButton(self, command=self.save_to_notes, text="Save to Notes")
        self.save_button.grid(row=4, column=0, columnspan=4, sticky="nsew", padx=20, pady=10)
        self.save_button.grid_remove()  # Hide the button initially


    def export_book(self):
        """ Export button callback """
        book_link = str(self.link_entry.get())

        print(f"book_link: {book_link}")
        book_data = library.get_book(book_link)

        status_msg = json.dumps(book_data, indent=2, ensure_ascii=False)
        self.status_label.configure(text=status_msg)

        res = library.export_book(book_data)
        result_json = json.loads(res.text)
        status_msg += "\n\ncode: " + str(res.status_code)
        status_msg += "\nresult: " + json.dumps(result_json, indent=2, ensure_ascii=False)

        self.status_label.configure(text=status_msg)

    def grab_data(self):
        """ Preview button callback """
        book_link = str(self.link_entry.get())

        print(f"book_link: {book_link}")
        book_data = library.get_book(book_link)

        if book_data:
            # Store the book data for later use
            self.current_book_data = book_data

            # Format book data as a table
            table = self.format_book_data_as_table(book_data)

            # Display the table
            self.status_label.configure(text=table)

            # Display the book cover image if available
            if 'image_name' in book_data and book_data['image_name']:
                self.display_book_image(book_data['image_name'])

            # Show the Save to Notes button
            self.save_button.grid()

            print(f"Previewed book: {book_data.get('title_clean', 'Unknown title')}")
        else:
            self.status_label.configure(text="Could not retrieve book data. Please check the URL.")
            # Hide the Save to Notes button if no book data
            self.save_button.grid_remove()

    def format_book_data_as_table(self, book_data):
        """ Format book data as a table """
        table = f"Book Information:\n{'=' * 50}\n"

        # Add title
        if 'title' in book_data:
            table += f"Title: {book_data['title']}\n"
        if 'title_clean' in book_data:
            table += f"Title (clean): {book_data['title_clean']}\n"

        # Add authors
        if 'authors' in book_data and book_data['authors']:
            authors = ", ".join(book_data['authors']) if isinstance(book_data['authors'], list) else book_data['authors']
            table += f"Author(s): {authors}\n"

        # Add a publishing house
        if 'publishing_house' in book_data:
            table += f"Publisher: {book_data['publishing_house']}\n"

        # Add year
        if 'year' in book_data and book_data['year']:
            table += f"Year: {book_data['year']}\n"

        # Add pages
        if 'pages' in book_data and book_data['pages']:
            table += f"Pages: {book_data['pages']}\n"

        # Add ISBN
        if 'isbn' in book_data and book_data['isbn']:
            table += f"ISBN: {book_data['isbn']}\n"

        # Add a link
        if 'link' in book_data:
            table += f"Link: {book_data['link']}\n"

        return table

    def display_book_image(self, image_name):
        """ Display book cover image """
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

                # Convert to PhotoImage
                photo = ImageTk.PhotoImage(img)

                # Create or update image label
                if hasattr(self, 'image_label'):
                    self.image_label.configure(image=photo)
                    self.image_label.image = photo
                else:
                    self.image_label = ctk.CTkLabel(master=self, text="", image=photo)
                    self.image_label.grid(row=3, column=0, columnspan=4, sticky="nsew", padx=20, pady=20)
                    self.image_label.image = photo
            except Exception as e:
                print(f"Error displaying image: {e}")

    def save_to_notes(self):
        """ Save book data to the Obsidian """

        result_message = library.save_to_notes()

        self.status_label.configure(text=result_message)
        print(result_message)


if __name__ == '__main__':
    app = App()
    app.mainloop()
