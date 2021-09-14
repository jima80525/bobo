#!/usr/bin/env python3
import PySimpleGUI as sg
sg.theme('Dark Amber')    # Add some color for fun

info = [
   {"date" : "03/09/2021", "series" : "",                "title" : "The Mirror and The Light",   "author" : "Hilary Mantel" },
   {"date" : "03/13/2021", "series" : "Memory Man",      "title" : "The Fix",                    "author" : "David Baldacci" },
   {"date" : "03/15/2021", "series" : "Jack Reacher",    "title" : "Worth Dying For",            "author" : "Lee Child" },
   {"date" : "03/19/2021", "series" : "Memory Man",      "title" : "The Last Mile",              "author" : "David Baldacci" },
   {"date" : "03/25/2021", "series" : "Memory Man",      "title" : "Redemption",                 "author" : "David Baldacci" },
   {"date" : "03/29/2021", "series" : "",                "title" : "Dance Hall of the Dead",     "author" : "Tony Hillerman" },
   {"date" : "04/04/2021", "series" : "Jack Reacher",    "title" : "Night School",               "author" : "Lee Child" },
   {"date" : "04/09/2021", "series" : "Atlee Pine",      "title" : "A Minute To Midnight",       "author" : "David Baldacci" },
   {"date" : "04/17/2021", "series" : "Archer",          "title" : "One Good Deed",              "author" : "David Baldacci" },
   {"date" : "04/28/2021", "series" : "",                "title" : "Chances Are",                "author" : "Richard Russo" },
   {"date" : "05/05/2021", "series" : "Jack Reacher",    "title" : "A Wanted Man",               "author" : "Lee Child" },
   {"date" : "05/12/2021", "series" : "",                "title" : "All the Devils Are Here",    "author" : "Louise Penny" },
   {"date" : "05/18/2021", "series" : "Will Robie",      "title" : "The Innocent",               "author" : "David Baldacci" },
   {"date" : "05/xx/2021", "series" : "Will Robie",      "title" : "The Target",                 "author" : "David Baldacci" },
   {"date" : "06/09/2021", "series" : "Jack Reacher",    "title" : "The Hard Way",               "author" : "Lee Child" },
   {"date" : "06/16/2021", "series" : "Jesse Stone",     "title" : "Night Passage",              "author" : "Robert B. Parker" },
   {"date" : "06/20/2021", "series" : "Spencer",         "title" : "God Save the Child",         "author" : "Robert B. Parker" },
   {"date" : "06/23/2021", "series" : "Jesse Stone",     "title" : "Night and Day",              "author" : "Robert B. Parker" },
   {"date" : "07/01/2021", "series" : "Sunny Randall",   "title" : "Family Honor",               "author" : "Robert B. Parker" },
   {"date" : "07/02/2021", "series" : "Sunny Randall",   "title" : "Perish Twice",               "author" : "Robert B. Parker" },
   {"date" : "07/03/2021", "series" : "Sunny Randall",   "title" : "Shrink Rap",                 "author" : "Robert B. Parker" },
   {"date" : "07/04/2021", "series" : "Sunny Randall",   "title" : "Melancholy Baby",            "author" : "Robert B. Parker" },
   {"date" : "07/05/2021", "series" : "Sunny Randall",   "title" : "Blue Screen",                "author" : "Robert B. Parker" },
   {"date" : "07/08/2021", "series" : "Sunny Randall",   "title" : "Spare Change",               "author" : "Robert B. Parker" },
   {"date" : "07/10/2021", "series" : "Jesse Stone",     "title" : "Killing the Blues",          "author" : "Michael Brandman" },
   {"date" : "07/11/2021", "series" : "Jesse Stone",     "title" : "Damned if you Do",           "author" : "Michael Brandman" },
   {"date" : "07/16/2021", "series" : "Jesse Stone",     "title" : "The Devil Wins",             "author" : "Reed Farrel Coleman" },
   {"date" : "07/18/2021", "series" : "Jesse Stone",     "title" : "Split Image",                "author" : "Robert B. Parker" },
   {"date" : "07/20/2021", "series" : "Spenser",         "title" : "Looking For Rachel Wallace", "author" : "Robert B. Parker" },
   {"date" : "07/28/2021", "series" : "Jack Reacher",    "title" : "The Sentinel",               "author" : "Lee Child" },
   {"date" : "07/30/2021", "series" : "Spenser",         "title" : "The Godwulf Manuscript",     "author" : "Robert B. Parker" },
   {"date" : "08/01/2021", "series" : "Jesse Stone",     "title" : "The Bitterest Pill",         "author" : "Reed Farrel Coleman" },
   {"date" : "08/07/2021", "series" : "Jesse Stone",     "title" : "The Hangman's Sonnet",       "author" : "Reed Farrel Coleman" },
   {"date" : "08/15/2021", "series" : "Jack Reacher",    "title" : "One Shot",                   "author" : "Lee Child" },
   {"date" : "08/19/2021", "series" : "Jesse Stone",     "title" : "High Profile",               "author" : "Robert B. Parker" },
   {"date" : "08/20/2021", "series" : "Jesse Stone",     "title" : "Stranger in Paradise",       "author" : "Robert B. Parker" },
   {"date" : "08/22/2021", "series" : "Spenser",         "title" : "Early Autumn",               "author" : "Robert B. Parker" },
   {"date" : "08/31/2021", "series" : "Will Robie",      "title" : "The Guilty",                 "author" : "David Baldacci" },
   {"date" : "09/03/2021", "series" : "Matthew Scudder", "title" : "The Sins of the Father",     "author" : "Lawrence Block" },
   {"date" : "09/07/2021", "series" : "Matthew Scudder", "title" : "In the Midst of Death",      "author" : "Lawrence Block" },
]
data = [[item["date"], item["author"], item["title"], item["series"]] for item in sorted(info, key=lambda x: x["date"], reverse=True)]

# Todo - make author and series filter drop-downs
# add labels for drop downs
# get keyboard shortcuts working


# 1- the layout
layout = [[sg.Text('Your typed chars appear here:'), sg.Text(size=(15,1), key='-OUTPUT-')],
          [sg.Input(key='-AUTHOR-'), sg.Input(key="-SERIES-")],
          [sg.Table(
                values=data,
                headings=["Date Read", "Author", "Title", "Series", ],
                key="-BOOKTABLE-",
                # hide_vertical_scroll=True,
                # row_height=15,
                # col_widths=100
          )],
          [sg.Button('Show'), sg.Button('Exit')]]

# 2 - the window
window = sg.Window('Pattern 2', layout)

# 3 - the event loop
while True:
    event, values = window.read()
    print(event, values)
    if event == sg.WIN_CLOSED or event == 'Exit':
        break
    if event == 'Show':
        # Update the "output" text element to be the value of "input" element
        print("author", values["-AUTHOR-"])
        print("series", values["-SERIES-"])
        author = values["-AUTHOR-"]
        series = values["-SERIES-"]
        data = [[item["date"], item["author"], item["title"], item["series"]] for item in sorted(info, key=lambda x: x["date"], reverse=True)]
        if author:
            data = [x for x in data if x[1] == author]
        if series:
            data = [x for x in data if x[3] == series]

        # window['-OUTPUT-'].update(values['-AUTHOR-'])
        window["-BOOKTABLE-"].update(data)

        # In older code you'll find it written using FindElement or Element
        # window.FindElement('-OUTPUT-').Update(values['-IN-'])
        # A shortened version of this update can be written without the ".Update"
        # window['-OUTPUT-'](values['-IN-'])

# 4 - the close
window.close()
