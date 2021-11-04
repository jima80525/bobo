#!/usr/bin/env python3
import dataclasses
import json
import pathlib
import PySimpleGUI as sg
import shutil
import sys
import time

sg.theme("Dark Amber")  # Add some color for fun

# TODO
# * add way to search for author or series in upper boxes - big lists is unwieldy

RETURN = chr(13)  # 13 is return char in ascii
ESC = chr(27)  # 27 is escape char in ascii
SORT_KEY = "date"
SORT_REVERSE = True


@dataclasses.dataclass
class Book:
    title: str
    author: str
    series: str
    date: str


class BookList:
    database_file = pathlib.Path("book.json")

    def __init__(self):
        self.sort_key = "date"
        self.sort_reverse = True
        self.full_info = self.read_data()
        self.update_data(True)

    def update_data(self, refresh):
        if refresh:
            self.full_authors = sorted(list({item["author"] for item in sorted(self.full_info, key=lambda x: x["author"])}))
            self.full_series = sorted(list(
                {item["series"] for item in sorted(self.full_info, key=lambda x: x["series"]) if item["series"]}
            ))
            self.authors = self.full_authors
            self.series = self.full_series
        self.data = []
        for item in sorted(self.full_info, key=lambda x: x[SORT_KEY], reverse=SORT_REVERSE):
            author_match = not self.authors or item["author"] in self.authors
            series_match = not self.series or not item["series"] or item["series"] in self.series
            print(f"{item['series']} list {self.series} {series_match}")
            if author_match and series_match:
                self.data.append(
                    [item["title"], item["author"], item["series"], item["date"]]
                )

    def read_data(self):
        data = None
        if self.database_file.is_file():
            with open(self.database_file, "r") as fp:
                data = json.load(fp)

        if not data or len(data) == 0:
            new_book = book_dialog("Add Book", [], [])
            if not new_book:
                print("No book information present")
                sys.exit()
            data = [
                {
                    "title": new_book.title,
                    "author": new_book.author,
                    "date": new_book.date,
                    "series": new_book.series,
                }
            ]
            self.full_info = data
            self.write_data()

        return data


    def write_data(self):
        if self.database_file.is_file():
            backup_dir = pathlib.Path("BACKUP")
            backup_dir.mkdir(exist_ok=True)
            backup_name = time.strftime("%Y_%m_%d_%H_%M_%S_") + str(self.database_file)
            backup_file = backup_dir / backup_name
            shutil.copy(self.database_file, backup_file)

        with open(self.database_file, "w") as fp:
            json.dump(self.full_info, fp, indent=2)

    def add_book(self, new_book):
        if new_book.title and new_book.author:
            self.full_info.append(
                {
                    "title": new_book.title,
                    "author": new_book.author,
                    "date": new_book.date,
                    "series": new_book.series,
                }
            )
            print("writing data")
            self.write_data()
            self.update_data(True)

    def edit_book(self, old_book, new_book):
        for item in self.full_info:
            test_book = Book(item["title"], item["author"], item["series"], item["date"])
            if test_book == old_book:
                print("Updating: ", old_book, " to ", new_book)
                item["title"] = new_book.title
                item["author"] = new_book.author
                item["date"] = new_book.date
                item["series"] = new_book.series
                self.write_data()
                self.update_data(True)

    def delete_book(self, book):
        for index, item in enumerate(self.full_info):
            test_book = Book(item["title"], item["author"], item["series"], item["date"])
            if test_book == book:
                print("Deleting: ", book, type(self.full_info))
                del self.full_info[index]
                self.write_data()
                self.update_data(True)

    def author_filter(self, author):
        self.authors = [author]
        self.series = [item["series"] for item in self.full_info if item["author"] in self.authors]
        self.update_data(False)

    def series_filter(self, series):
        self.series = [series]
        self.authors = [item["author"] for item in self.full_info if item["series"] and item["series"] in self.series]
        self.update_data(False)

    def clear_filters(self):
        self.authors = self.full_authors
        self.series = self.full_series
        self.update_data(True)

def delete_dialog(book):
    result = sg.popup_yes_no(f"Delete {book.title} by {book.author}?")
    return result == "Yes"

def book_dialog(dialog_title, authors, series, book=None):
    authors_combo = sg.Combo(authors, key="-AUTH-", expand_x=True)
    series_combo = sg.Combo(series, key="-SER-", expand_x=True)
    layout = [
        [sg.Text("Title:"), sg.Input(key="-TITLE-")],
        [
            sg.CalendarButton("Date Finished", format="%m/%d/%Y", key="-CAL-", enable_events=True),
            sg.Text("Not Set", key="-DATE-"),
        ],
        [sg.Text("Author:"), authors_combo],
        [sg.Text("Series:"), series_combo],
        [sg.OK(key="Ok"), sg.Cancel(key="Cancel")],
    ]
    window = sg.Window(dialog_title, layout=layout, return_keyboard_events=True)
    window.finalize()  # obligatory to allow updating boxes
    if book and book.title:
        window["-TITLE-"].update(value=book.title)
    if book and book.author:
        window["-AUTH-"].update(value=book.author)
    if book and book.series:
        window["-SER-"].update(value=book.series)
    if book and book.date:
        window["-DATE-"].update(value=book.date)
    title = None
    author = None
    while True:
        event, values = window.read()
        if event in [sg.WIN_CLOSED, "Cancel", ESC]:
            window.close()
            return None

        if event == "-CAL-":
            date_text = window["-DATE-"]
            date_text.update(values["-CAL-"])

        if event in ["Ok", RETURN]:
            title = values["-TITLE-"]
            cal = window["-DATE-"].get()
            if cal == "Not Set":
                cal = ""
            author = values["-AUTH-"]
            series = values["-SER-"]
            window.close()
            if title and author:  # must supply title and author
                return Book(title, author, series, cal)
            return None


def update_ui(window, books):
    window["-AUTHORS-"].update(books.authors)
    window["-SERIES-"].update(books.series)
    window["-BOOKTABLE-"].update(books.data)
    table = window["-BOOKTABLE-"]
    if len(table.Values):
        table.update(select_rows=[0])


books = BookList()

layout = [
    [
        sg.Text("Filter by author:"),
        sg.Listbox(values=books.authors, size=(50, 10), key="-AUTHORS-", enable_events=True),
        sg.Text("Filter by series:"),
        sg.Listbox(values=books.series, size=(50, 10), key="-SERIES-", enable_events=True),
    ],
    [
        sg.Table(
            values=books.data,
            headings=[
                "Title",
                "Author",
                "Series",
                "Date Read",
            ],
            justification="center",
            expand_x=True,
            expand_y=True,
            key="-BOOKTABLE-",
            enable_events=True,
            change_submits=True,
            selected_row_colors="red on yellow",
            select_mode=sg.TABLE_SELECT_MODE_BROWSE,
        )
    ],
    [sg.Button("Clear Filters"), sg.Button("Add"), sg.Button("Exit")],
]
window = sg.Window("Book of Books", layout, return_keyboard_events=True, resizable=True)
window.finalize()
table = window["-BOOKTABLE-"]
table.block_focus(False)
table.update(select_rows=[0])
table.bind("<Button-1>", "Click")

while True:
    event, values = window.read()
    # print(event, values)
    if event in [sg.WIN_CLOSED, "Exit", ESC]:
        break
    elif event == 'Clear Filters':
        books.clear_filters()
        update_ui(window, books)
    elif event == '-BOOKTABLE-Click':
        e = table.user_bind_event
        region = table.Widget.identify('region', e.x, e.y)
        if region == 'heading':
            sort_indices = [ "title", "author", "series", "date", ] # JHA TODO probably should find a way to only encode this one place
            column = int(table.Widget.identify_column(e.x)[1:]) - 1
            SORT_KEY = sort_indices[column]
            SORT_REVERSE = not SORT_REVERSE
            update_ui(window, books)
    elif event == '-AUTHORS-':
        books.author_filter(values["-AUTHORS-"][0])
        update_ui(window, books)
    elif event == '-SERIES-':
        books.series_filter(values["-SERIES-"][0])
        update_ui(window, books)
    elif event in ["Add", "a", "A"]:
        new_book = book_dialog("Add Book", books.full_authors, books.full_series)
        if new_book is not None:
            books.add_book(new_book)
            update_ui(window, books)
    elif event in ["Edit", "e", "E"]:
        if table and table.SelectedRows:
            if table.SelectedRows:
                book = Book(*table.Values[table.SelectedRows[0]])
                new_book = book_dialog("Edit Book", books.full_authors, books.full_series, book)
                if new_book is not None:
                    books.edit_book(book, new_book)
                    update_ui(window, books)
    elif event in ["Delete", "d", "D"]:
        if table and table.SelectedRows:
            if table.SelectedRows:
                book = Book(*table.Values[table.SelectedRows[0]])
                if delete_dialog(book):
                    books.delete_book(book)
                    update_ui(window, books)

window.close()
