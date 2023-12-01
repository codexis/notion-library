""" Main window Python script of the Library Project """
import json
import customtkinter as ctk
from service.library import Library

library = Library()


class App(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.geometry("800x600")
        self.title("Notion Library")

        self.top_label = ctk.CTkLabel(master=self, width=200, height=100, text="Notion Library Exporter")
        self.top_label.grid(row=0, column=1, sticky="nsew")

        self.link_label = ctk.CTkLabel(master=self, width=150, text="Book ID to export")
        self.link_label.grid(row=1, column=0, sticky="nsew")

        self.link_entry = ctk.CTkEntry(master=self, width=200)
        self.link_entry.insert("0", "1003006746")
        self.link_entry.grid(row=1, column=1, sticky="nsew")

        self.button = ctk.CTkButton(self, command=self.export_book, text="Export")
        self.button.grid(row=1, column=2, padx=20, pady=10)

        self.status_label = ctk.CTkLabel(master=self, width=550, text="", justify="left")
        self.status_label.grid(row=2, column=0, columnspan=3, sticky="nsew", padx=20, pady=20)

    # add methods to app
    def export_book(self):
        book_id = int(self.link_entry.get())
        book_data = library.get_book(book_id)

        status_msg = json.dumps(book_data, indent=2, ensure_ascii=False)
        self.status_label.configure(text=status_msg)

        res = library.export_book(book_data)
        result_json = json.loads(res.text)
        status_msg += "\n\ncode: " + str(res.status_code)
        status_msg += "\nresult: " + json.dumps(result_json, indent=2, ensure_ascii=False)

        self.status_label.configure(text=status_msg)


if __name__ == '__main__':
    app = App()
    app.mainloop()
