#!/usr/bin/env python3
import json
import pathlib
import matplotlib.pyplot as plt
from collections import defaultdict
# plt.plot(["feb", "mar", "apr", "may"], [1, 4, 9, 16])
# plt.ylabel('some numbers')
# plt.show()

def read_data(database_file):
    if database_file.is_file():
        with open(database_file, "r") as fp:
            data = json.load(fp)
    return data
#
# def write_data(database_file, data):
    # with open(database_file, "w") as fp:
        # json.dump(data, fp, indent=2)
#

database_file = pathlib.Path("book.json")
data = read_data(database_file)
print(f"Read {len(data)} records")
#
hist = defaultdict(int)
for book in data:
    if book["date"]:
        year = book["date"].split("/")[0]
        hist[year] += 1
#
# print(hist)
# for key in sorted(hist):
    # print

years = [key for key in sorted(hist)]
values = [hist[key] for key in sorted(hist)]
# print(years)
# print(values)
plt.plot(years, values)
plt.ylabel('number read')
plt.show()
#
# write_data(database_file, data)

# item = {}
# item["title"] = "t"
# item["author"] = "a"
# item["series"] = "s"
# item["date"] = "d"
# item["audiobook"] = "b"
# print(item)
# print(list(item.values()))
