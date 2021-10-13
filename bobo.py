#!/usr/bin/env python3
import json
import PySimpleGUI as sg
sg.theme('Dark Amber')    # Add some color for fun

database_file = "book.json"
def read_data():
    with open(database_file, "r") as fp:
        return json.load(fp)


def write_data(info):
    with open(database_file, "w") as fp:
        json.dump(info, fp, indent=2)


def book_dialog(dialog_title, authors, series, book_info=(None, None, None, None)):
    init_title, init_author, init_date, init_series = book_info
    authors_combo = sg.Combo(authors, key='-AUTH-')
    series_combo = sg.Combo(series, key='-SER-')
    layout = [
        [sg.Text("Title:"), sg.Input(key="-TITLE-")],
        [sg.CalendarButton("Date Finished", format="%m/%d/%Y", key="-CAL-", enable_events=True), sg.Text("Not Set", key="-DATE-")],
        [sg.Text("Author:"), authors_combo],
        [sg.Text("Series:"), series_combo],
        [sg.OK(key="Ok"), sg.Cancel(key="Cancel")]
    ]
    window = sg.Window(dialog_title, layout=layout, return_keyboard_events=True)
    window.finalize()  # obligatory to allow updating boxes
    if init_title:
        window["-TITLE-"].update(value=init_title)
    if init_author:
        window["-AUTH-"].update(value=init_author)
    if init_date:
        window["-DATE-"].update(value=init_date)
    if init_series:
        window["-SER-"].update(value=init_series)
    title = None
    author = None
    while True:
        event, values = window.read()
        print(event, values)
        if event in [sg.WIN_CLOSED, "Cancel", chr(27)]:  # 27 is escape char in ascii
            window.close()
            return None, None, None, None
        if event == "-CAL-":
            date_text = window["-DATE-"]
            date_text.update(values["-CAL-"])

        if event == 'Ok':
            title = values['-TITLE-']
            cal = window['-DATE-'].get()
            if cal == "Not Set":
                cal = ""
            author = values['-AUTH-']
            series = values['-SER-']
            window.close()
            if title and author:  # must supply title and author
                return title, cal, author, series
            return None, None, None, None


def add_book(dialog_title, authors, series):
    return book_dialog("Add Book", authors, series)


def edit_book(authors, full_series, book_info):
    # title, author, date, series = book_info
    # return book_dialog("Edit Book", authors, full_series, init_title=title, init_author=author, init_date=date, init_series=series)
    return book_dialog("Edit Book", authors, full_series, book_info)


def build_lists(info):
    authors = list({item["author"] for item in sorted(info, key=lambda x: x["author"])})
    series = list({item["series"] for item in sorted(info, key=lambda x: x["series"]) if item["series"]})
    data = [[item["title"], item["author"], item["date"], item["series"]] for item in sorted(info, key=lambda x: x["date"], reverse=True)]
    return authors, series, data

info = read_data()
full_authors, full_series, full_data = build_lists(info)

# Todo
# edit existing record
# back up file before writintable g

layout = [[sg.Text("Filter by author:"), sg.Listbox(values=list(full_authors), size=(50,10), key='-AUTHORS-', enable_events=True),
          sg.Text("Filter by series:"), sg.Listbox(values=list(full_series), size=(50,10), key='-SERIES-', enable_events=True),],
          [sg.Table(values=full_data, headings=["Title", "Author", "Date Read", "Series", ], justification="center", expand_x=True, expand_y=True,key="-BOOKTABLE-", enable_events=True, selected_row_colors="red on yellow", select_mode=sg.TABLE_SELECT_MODE_BROWSE)],
          [sg.Button('Clear Filters'), sg.Button('Add'), sg.Button('Exit')]]
window = sg.Window('Book of Books', layout, return_keyboard_events=True, resizable=True)
window.finalize()
window.maximize()
table = window["-BOOKTABLE-"]
table.update(select_rows=[0])


while True:
    event, values = window.read()
    print(event)
    if event == sg.WIN_CLOSED or event == 'Exit':
        break
    if event == 'Clear Filters':
        window["-AUTHORS-"].update(full_authors) # JHA TODO handle multiple selection in both?
        window["-SERIES-"].update(full_series)
        window["-BOOKTABLE-"].update(full_data)

    if event in ('-AUTHORS-', '-SERIES-'):
        # Update the "output" text element to be the value of "input" element
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
            window["-AUTHORS-"].update([author]) # JHA TODO handle multiple selection in both?
            new_series = {item["series"] for item in info if item["author"] == author}
            window["-SERIES-"].update(list(new_series))
        if series:
            data = [x for x in data if x[3] == series]
            window["-SERIES-"].update([series])
            new_authors = {item["author"] for item in info if item["series"] == series}
            window["-AUTHORS-"].update(list(new_authors))

        window["-BOOKTABLE-"].update(data)
    if event in ['Add', 'a', 'A']:
        title, cal, author, series = add_book("Add New Book", sorted(full_authors), sorted(full_series))
        if title and author:
            info.append({
                "date": cal,
                "series": series,
                "title": title,
                "author": author,
            })
            write_data(info)
            full_authors, full_series, full_data = build_lists(info)
            window["-AUTHORS-"].update(full_authors)
            window["-SERIES-"].update(full_series)
            window["-BOOKTABLE-"].update(full_data)
    if event in ['Edit', 'e', 'E']:
        if table and table.SelectedRows:
            if table.SelectedRows:
                edit_book(full_authors, full_series, table.Values[table.SelectedRows[0]])


window.close()
