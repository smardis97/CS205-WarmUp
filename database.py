import sqlite3

cities = []


def read_to_database():
    global cities
    data_file = open("US_Cities.csv")
    text = data_file.read()
    entries = [[]]
    next_entry = ""
    nl_count = 0
    for char in text:
        if char != '\n' and char != ',':
            next_entry += char
        else:
            entries[nl_count].append(next_entry)
            next_entry = ""
        if char == '\n':
            print(nl_count)
            nl_count += 1
            entries.append([])

    for entry in entries:
        if entry[0] != "city":
            cities.append([entry[0], entry[3], parse_to_int(entry[8]), float(entry[10]), entry[13]])

    


def parse_to_int(string):
    if string == '':
        return -1
    else:
        return int(string)


conn = sqlite3.connect('database.db')

cur = conn.cursor()

read_to_database()
# cur.execute(
#     "CREATE TABLE Cities (city_name text, state text, population integer, density real, timezone text,"
#     " PRIMARY KEY (city_name), FOREIGN KEY (state) States(state_name))")
#
# cur.execute(
#     "CREATE TABLE States (state_name text, capital_city text,"
#     " PRIMARY KEY (state_name), FOREIGN KEY (capital_city) Cities(city_name))")


