#!/usr/bin/env python3
import json
import pathlib

def read_data(database_file):
    books = []
    if database_file.is_file():
        with open(database_file, "r") as fp:
            for line in fp.readlines():
                line = line.strip()
                date, title, author = line.split(" -")
                series = ""
                if "+" in title:
                    series, title = title.split("+")

                m,d,y = date.split("/")
                date = f"{y}/{m}/{d}"
                print(f"auth {author} date {date} title {title} series {series}")

                book = {
                    "title": title,
                    "author": author,
                    "date": date,
                    "series": series,
                    "audiobook": True,
                }
                books.append(book)
    return books

def write_data(database_file, data):
    with open(database_file, "w") as fp:
        json.dump(data, fp, indent=2)


database_file = pathlib.Path("audio.txt")
data = read_data(database_file)
#
# for book in data:
    # book["audiobook"] = False
#
#
write_data("audio.json", data)

# item = {}
# item["title"] = "t"
# item["author"] = "a"
# item["series"] = "s"
# item["date"] = "d"
# item["audiobook"] = "b"
# print(item)
# print(list(item.values()))
