import sqlite3
import csv


conn = sqlite3.connect('database.db')
cur = conn.cursor()


def read_to_database():
    # state_population functions as a dictionary, where the state name is the key,
    # and the the population is the value. When the data from the csv is read using
    # the below code, the key is identifed when a particular cell in the
    # state_name row is read. Where the value for a partular state in state_population
    # is edited in the dictionary depends on the state_name read from the csv.
    # If state for a city is "New York", then the value for 'New York' in the
    # state_population dictionary will change, and not say 'Vermont'.
    # At the end of reading the csv, this will contain the state population
    # for every single state, effectively adding a state population section
    # without having the state population data beforehand.
    state_population = {
        'Alabama': 0,
        'Alaska': 0,
        'Arizona': 0,
        'Arkansas': 0,
        'California': 0,
        'Colorado': 0,
        'Connecticut': 0,
        'Delaware': 0,
        'District of Columbia': 0,
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

    # These are hard coded into the database, has no interaction from the csv.
    # This is a dictionary where the key is the state, and the value is the
    # capital of the state
    state_capitals = {
        'Alabama': 'Montgomery',
        'Alaska': 'Juneau',
        'Arizona': 'Phoenix',
        'Arkansas': 'Little Rock',
        'California': 'Sacramento',
        'Colorado': 'Denver',
        'Connecticut': 'Hartford',
        'Delaware': 'Dover',
        'District of Columbia': 'Washington',
        'Florida': 'Tallahassee',
        'Georgia': 'Atlanta',
        'Hawaii': 'Honolulu',
        'Idaho': 'Boise',
        'Illinois': 'Springfield',
        'Indiana': 'Indianapolis',
        'Iowa': 'Des Moines',
        'Kansas': 'Topeka',
        'Kentucky': 'Frankfort',
        'Louisiana': 'Baton Rouge',
        'Maine': 'Augusta',
        'Maryland': 'Annapolis',
        'Massachusetts': 'Boston',
        'Michigan': 'Lansing',
        'Minnesota': 'Saint Paul',
        'Mississippi': 'Jackson',
        'Missouri': 'Jefferson City',
        'Montana': 'Helena',
        'Nebraska': 'Lincoln',
        'Nevada': 'Carson City',
        'New Hampshire': 'Concord',
        'New Jersey': 'Trenton',
        'New Mexico': 'Santa Fe',
        'New York': 'Albany',
        'North Carolina': 'Raleigh',
        'North Dakota': 'Bismarck',
        'Ohio': 'Columbus',
        'Oklahoma': 'Oklahoma City',
        'Oregon': 'Salem',
        'Pennsylvania': 'Harrisburg',
        'Rhode Island': 'Providence',
        'South Carolina': 'Columbia',
        'South Dakota': 'Pierre',
        'Tennessee': 'Nashville',
        'Texas': 'Austin',
        'Utah': 'Salt Lake City',
        'Vermont': 'Montpelier',
        'Virginia': 'Richmond',
        'Washington': 'Olympia',
        'West Virginia': 'Charleston',
        'Wisconsin': 'Madison',
        'Wyoming': 'Cheyenne'
    }

    cities = []
    data_file = open("US_Cities.csv")
    entries = csv.reader(data_file, delimiter=',')
    # reads into the csv and retrieves the data

    for entry in entries:
        if entry[0] != "city":  # skip header line, the line with the city, city_ascii,
                                # state_id, and so on

            # the line below reads into the the csv for every remaining line in the file,
            # where enrty[0] is the city row of the csv,
            # entry[3] is the state_name row, entry[8] is the population row,
            # entry[10] is the density row, and entry[13] is the timezone row.

            cities.append([entry[0], entry[3], parse_to_int(entry[8]), float(entry[10]), entry[13]])

            # Construct cities = [[city, state, population, density, timezone]]
            # cities becomes a 2D array here 
            # parse_to_int and float are used on entry[8] and entry[10] respectively since
            # all of the data in the csv are regarded by default as strings, and needs to be
            # converted to the correct type so they will be seen as numbers and can be used
            # as such.

    for city in cities:
        if city[2] != -1:  # -1 indicates the csv had no population data for that city, as some cells
                           # in the csv for population are blank
            state_population[city[1]] += city[2]
            # Count population of each state

    # add cities to the Cities table
    for city in cities:
        
        cur.execute("INSERT INTO Cities VALUES (?, ?, ?, ?, ?)", (city[0], city[1], city[2], city[3], city[4]))
        #the categories for the cities table in this for loop are as in the "Contstruct Cities"
        #comment above, where city[0] is city, city[1] is state, and so forth

    # add states to the States table
    for state in state_population:
        # rowid is built in unique id in sqlite
        # this puts the state and state captial into the database

        cur.execute("SELECT rowid FROM Cities WHERE state = ? AND city_name = ?", (state, state_capitals[state]))
        unique_id = cur.fetchone()[0]
        cur.execute("INSERT INTO States VALUES (?, ?, ?)", (state, unique_id, state_population[state]))

# this is used when reading into the csv. In our csv file, some of the lines are blank,
# meaning there is nothing in the cell. This function serves to check to see if the cell
# being checked is empty or not, as all the "cells" of our database need to hold something,
# even if there is nothing available from the csv cell to put into a certain "cell" of our database.
# When a cell read from the csv is blank, this function returns a value of -1 to put into the database, so it knows that
# this cell is blank. Otherwise it returns the value converted into an integer, as all the data read from the csv is considered
# a string, and needs to be converted to the correct data type.
 
def parse_to_int(string):
    if string == '':
        return -1
    else:
        return int(string)


#this deletes the database.db file, then reads from the csv file and reinitializes 
def reinit_database():
    global cur

    try:
        cur.execute("DROP TABLE Cities")
        cur.execute("DROP TABLE States")
    except sqlite3.OperationalError:
        pass

    # Cities table uses built in ROWID as primary key
    cur.execute(
        "CREATE TABLE Cities (city_name text, state text,"
        " population integer, density real, timezone text,"
        " FOREIGN KEY (state) REFERENCES States(state_name))")

    cur.execute(
        "CREATE TABLE States (state_name text,"
        " capital_city_id int NOT NULL,"
        " state_population integer,"
        " PRIMARY KEY (state_name), FOREIGN KEY (capital_city_id) REFERENCES Cities(rowid))")

    read_to_database()
