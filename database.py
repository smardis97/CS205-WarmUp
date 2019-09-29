import sqlite3

cities = []
conn = sqlite3.connect('database.db')
cur = conn.cursor()
state_population = {
    'Alabama': 0,
    'Alaska': 0,
    'Arizona': 0,
    'Arkansas': 0,
    'California': 0,
    'Colorado': 0,
    'Connecticut': 0,
    'Delaware': 0,
    'Florida': 0,
    'Georgia': 0,
    'Hawaii': 0,
    'Idaho': 0,
    'Illinois': 0,
    'Indiana': 0,
    'Iowa': 0,
    'Kansas': 0,
    'Kentucky': 0,
    'Louisiana': 0,
    'Maine': 0,
    'Maryland': 0,
    'Massachusetts': 0,
    'Michigan': 0,
    'Minnesota': 0,
    'Mississippi': 0,
    'Missouri': 0,
    'Montana': 0,
    'Nebraska': 0,
    'Nevada': 0,
    'New Hampshire': 0,
    'New Jersey': 0,
    'New Mexico': 0,
    'New York': 0,
    'North Carolina': 0,
    'North Dakota': 0,
    'Ohio': 0,
    'Oklahoma': 0,
    'Oregon': 0,
    'Pennsylvania': 0,
    'Rhode Island': 0,
    'South Carolina': 0,
    'South Dakota': 0,
    'Tennessee': 0,
    'Texas': 0,
    'Utah': 0,
    'Vermont': 0,
    'Virginia': 0,
    'Washington': 0,
    'West Virginia': 0,
    'Wisconsin': 0,
    'Wyoming': 0
}


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
            # Construct cities = [[city, state, population, density, timezone]]

    for city in cities:
        if city[2] != -1:
            state_population[city[1]] += city[2]


def parse_to_int(string):
    if string == '':
        return -1
    else:
        return int(string)


def reinit_database():
    global cur

    cur.execute("DROP TABLE Cities")
    cur.execute("DROP TABLE States")

    cur.execute(
        "CREATE TABLE Cities (city_name text, state text, population integer, density real, timezone text,"
        " PRIMARY KEY (city_name), FOREIGN KEY (state) REFERENCES States(state_name))")

    cur.execute(
        "CREATE TABLE States (state_name text, capital_city text,"
        " PRIMARY KEY (state_name), FOREIGN KEY (capital_city) REFERENCES Cities(city_name))")


reinit_database()
read_to_database()
