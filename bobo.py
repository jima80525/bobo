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

def add_book(title, text, authors, series):
    # authors.insert(0, "New Author")
    window = sg.Window(title,
        [[sg.Text(text)],
        [sg.Text("Title:"), sg.Input(key="-TITLE-")],
        [sg.CalendarButton("Date Finished", format="%m/%d/%Y", key="-CAL-", enable_events=True),
        sg.Text("Not Set", key="-DATE-")],
        [sg.Combo(authors, key='-AUTH-'), sg.Combo(series, key='-SER-')],
            [sg.OK(key="Ok"), sg.Cancel(key="Cancel")]
    ], return_keyboard_events=True)
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



def build_lists(info):
    authors = list({item["author"] for item in sorted(info, key=lambda x: x["author"])})
    series = list({item["series"] for item in sorted(info, key=lambda x: x["series"]) if item["series"]})
    data = [[item["title"], item["author"], item["date"], item["series"]] for item in sorted(info, key=lambda x: x["date"], reverse=True)]
    return authors, series, data

info = read_data()
full_authors, full_series, full_data = build_lists(info)

# Todo
# edit existing record
# back up file before writing

# layout = [[sg.Text("Filter by author:"), sg.Listbox(values=list(full_authors), expand_x=True, expand_y=True, key='-AUTHORS-', enable_events=True),
        #   sg.Text("Filter by series:"), sg.Listbox(values=list(full_series),  expand_x=True, expand_y=True,key='-SERIES-', enable_events=True),],
layout = [[sg.Text("Filter by author:"), sg.Listbox(values=list(full_authors), size=(50,10), key='-AUTHORS-', enable_events=True),
          sg.Text("Filter by series:"), sg.Listbox(values=list(full_series), size=(50,10), key='-SERIES-', enable_events=True),],
          [sg.Table(values=full_data, headings=["Title", "Author", "Date Read", "Series", ], justification="center", expand_x=True, expand_y=True,key="-BOOKTABLE-", enable_events=True, selected_row_colors="red on yellow", select_mode=sg.TABLE_SELECT_MODE_BROWSE)],
          [sg.Button('Clear Filters'), sg.Button('Add'), sg.Button('Exit')]]
window = sg.Window('Book of Books', layout, return_keyboard_events=True, resizable=True)
window.finalize()
window.maximize()

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
        title, cal, author, series = add_book("Add Titles", "selection please", sorted(full_authors), sorted(full_series))
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
        table = window["-BOOKTABLE-"]
        if table and table.SelectedRows:
            print(table.SelectedRows)
            if table.SelectedRows:
                print(table.Values[table.SelectedRows[0]])


window.close()
