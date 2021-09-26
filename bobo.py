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

info = read_data()
data = [[item["date"], item["author"], item["title"], item["series"]] for item in sorted(info, key=lambda x: x["date"], reverse=True)]

# Todo
# get keyboard shortcuts working
# Multiple selection in filters?  Probably not
# add item - new dialog with author and series as drop down and none indicating
# it needs to be adde


full_authors = {item["author"] for item in sorted(info, key=lambda x: x["author"])}
full_series = {item["series"] for item in sorted(info, key=lambda x: x["series"]) if item["series"]}
full_data = [[item["date"], item["author"], item["title"], item["series"]] for item in sorted(info, key=lambda x: x["date"], reverse=True)]

layout = [[sg.Text("Filter by author:"), sg.Listbox(values=list(full_authors), size=(20,4), key='-AUTHORS-', enable_events=True),
          sg.Text("Filter by series:"), sg.Listbox(values=list(full_series), size=(20,4), key='-SERIES-', enable_events=True),],
          [sg.Table(values=full_data, headings=["Date Read", "Author", "Title", "Series", ], key="-BOOKTABLE-", enable_events=True)],
          [sg.Button('Clear Filters'), sg.Button('Exit')]]


window = sg.Window('Pattern 2', layout)

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

window.close()
