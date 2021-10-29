#!/usr/bin/env python3
import  dataclasses
import json
import pathlib
import PySimpleGUI as sg
import shutil
import sys
import time
sg.theme('Dark Amber')    # Add some color for fun

@dataclasses.dataclass
class Book:
    title: str
    author: str
    series: str
    date: str


database_file = pathlib.Path("book.json")

def read_data():
    if not database_file.is_file():
        return None
    with open(database_file, "r") as fp:
        return json.load(fp)


def write_data(info):
    if database_file.is_file():
        backup_dir = pathlib.Path("BACKUP")
        backup_dir.mkdir(exist_ok=True)
        backup_name = time.strftime("%Y_%m_%d_%H_%M_%S_") + str(database_file)
        backup_file = backup_dir / backup_name
        shutil.copy(database_file, backup_file)

    with open(database_file, "w") as fp:
        json.dump(info, fp, indent=2)


def book_dialog(dialog_title, authors, series, book=None):
    authors_combo = sg.Combo(authors, key='-AUTH-', expand_x=True)
    series_combo = sg.Combo(series, key='-SER-', expand_x=True)
    layout = [
        [sg.Text("Title:"), sg.Input(key="-TITLE-")],
        [sg.CalendarButton("Date Finished", format="%m/%d/%Y", key="-CAL-", enable_events=True), sg.Text("Not Set", key="-DATE-")],
        [sg.Text("Author:"), authors_combo],
        [sg.Text("Series:"), series_combo],
        [sg.OK(key="Ok"), sg.Cancel(key="Cancel")]
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
        if event in [sg.WIN_CLOSED, "Cancel", chr(27)]:  # 27 is escape char in ascii
            window.close()
            return None
        if event == "-CAL-":
            date_text = window["-DATE-"]
            date_text.update(values["-CAL-"])

        if event in ['Ok', chr(13)]:  # 13 is return in ascii
            title = values['-TITLE-']
            cal = window['-DATE-'].get()
            if cal == "Not Set":
                cal = ""
            author = values['-AUTH-']
            series = values['-SER-']
            window.close()
            if title and author:  # must supply title and author
                return Book(title, author, series, cal)
            return None


def update_info(info, old_book, new_book):
    for item in info:
        test_book = Book(item["title"], item["author"], item["date"], item["series"])
        if test_book == old_book:
            print("ADDING:")
            print(item)
            print(test_book)
            print(new_book)
            item["title"] = new_book.title
            item["author"] = new_book.author
            item["date"] = new_book.date
            item["series"] = new_book.series
            return info
    # old book not found - add it
    if new_book.title and new_book.author:
        info.append({
            "title": new_book.title,
            "author": new_book.author,
            "date": new_book.date,
            "series": new_book.series,
        })
    return info


def update_info_and_ui(window, info, old_book, new_book):
    global full_authors, full_series, full_data
    info = update_info(info, old_book, new_book)
    write_data(info)
    full_authors, full_series, full_data = build_lists(info)
    window["-AUTHORS-"].update(full_authors)
    window["-SERIES-"].update(full_series)
    window["-BOOKTABLE-"].update(full_data)
    table = window["-BOOKTABLE-"]
    table.update(select_rows=[0])


def build_lists(info):
    authors = list({item["author"] for item in sorted(info, key=lambda x: x["author"])})
    series = list({item["series"] for item in sorted(info, key=lambda x: x["series"]) if item["series"]})
    data = [[item["title"], item["author"], item["date"], item["series"]] for item in sorted(info, key=lambda x: x["date"], reverse=True)]
    return authors, series, data

info = read_data()
if not info:
    new_book = book_dialog("Add Book", [], [])
    if not new_book:
        print("No book information present")
        sys.exit()
    info = [{
        "title": new_book.title,
        "author": new_book.author,
        "date": new_book.date,
        "series": new_book.series,
    }]
    write_data(info)

full_authors, full_series, full_data = build_lists(info)

layout = [[sg.Text("Filter by author:"), sg.Listbox(values=list(full_authors), size=(50,10), key='-AUTHORS-', enable_events=True),
          sg.Text("Filter by series:"), sg.Listbox(values=list(full_series), size=(50,10), key='-SERIES-', enable_events=True),],
          [sg.Table(values=full_data, headings=["Title", "Author", "Date Read", "Series", ], justification="center", expand_x=True, expand_y=True, key="-BOOKTABLE-", enable_events=True, change_submits=True, selected_row_colors="red on yellow", select_mode=sg.TABLE_SELECT_MODE_BROWSE)],
          [sg.Button('Clear Filters'), sg.Button('Add'), sg.Button('Exit')]]
window = sg.Window('Book of Books', layout, return_keyboard_events=True, resizable=True)
window.finalize()
window.maximize()
table = window["-BOOKTABLE-"]
table.update(select_rows=[0])
table.block_focus(False)
table.set_focus(force=True)

while True:
    event, values = window.read()
    print(event, values)
    if event in [sg.WIN_CLOSED, "Exit", chr(27)]:  # 27 is escape char in ascii
        break
    if event == 'Clear Filters':
        window["-AUTHORS-"].update(full_authors)
        window["-SERIES-"].update(full_series)
        window["-BOOKTABLE-"].update(full_data)

    if event in ('-AUTHORS-', '-SERIES-'):
        data = full_data
        author = None
        series = None
        if values["-AUTHORS-"]:
            author = values["-AUTHORS-"][0]
        if values["-SERIES-"]:
            series = values["-SERIES-"][0]
        data = [[item["date"], item["author"], item["title"], item["series"]] for item in sorted(info, key=lambda x: x["date"], reverse=True)]
        if author:
            data = [x for x in data if x[1] == author]
            window["-AUTHORS-"].update([author])
            new_series = {item["series"] for item in info if item["author"] == author}
            window["-SERIES-"].update(list(new_series))
        if series:
            data = [x for x in data if x[3] == series]
            window["-SERIES-"].update([series])
            new_authors = {item["author"] for item in info if item["series"] == series}
            window["-AUTHORS-"].update(list(new_authors))

        window["-BOOKTABLE-"].update(data)
    if event in ['Add', 'a', 'A']:
        new_book = book_dialog("Add Book", sorted(full_authors), sorted(full_series))
        update_info_and_ui(window, info, None, new_book)
    if event in ['Edit', 'e', 'E']:
        if table and table.SelectedRows:
            if table.SelectedRows:
                book = Book(*table.Values[table.SelectedRows[0]])
                new_book = book_dialog("Edit Book", full_authors, full_series, book)
                update_info_and_ui(window, info, book, new_book)

window.close()
