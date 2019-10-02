from database import *

valid_commands = [
    'help',
    'exit',
    'reload',
    'population',
    'density',
    'timezone',
    'capital',
    'city',
    'state'
]


# In order to properly handle city and state names that contain more than one word,
# like "New York" and "Little Rock", we cannot simply divide the query by the space
# delimiter.
#
# Whenever validate_and_split finds a word in the query that is not one of the expected commands
# it assumes that it is part of a multi-part place name. It adds each non-command word after
# that until it encounters a valid command word, or reaches the end of the file.
# It then adds the entire name as a single element of the list, before moving of.
def validate_and_split(query):
    divided_query = []  # will contain the separated arguments
    next_block = ""
    last_word = ""
    multi_word = False
    for char in query:
        if char == " ":  # space is the argument delimiter
            if not multi_word:  # standard procedure when not expecting a name
                if not valid_commands.__contains__(next_block):  # if the new word is not a command
                    multi_word = True
                    last_word = next_block  # last word will contain all of the multi-part name
                    next_block = ""
                else:
                    divided_query.append(next_block)
                    next_block = ""
            else:  # if already expecting a name
                if not valid_commands.__contains__(next_block):  # next part of the name
                    last_word += " " + next_block
                    next_block = ""
                else:  # if next_block is a valid command, then the place name can be added
                    multi_word = False
                    divided_query.append(last_word)
                    divided_query.append(next_block)
                    last_word = ""
                    next_block = ""
        elif char == "%":  # % is the end character for the query
            if not multi_word:
                divided_query.append(next_block)
                next_block = ""
            else:  # ensures that multi-part names get added properly at the end of a query
                if not valid_commands.__contains__(next_block):
                    last_word += " " + next_block
                    next_block = ""
                    divided_query.append(last_word)
                    last_word = ""
                else:
                    multi_word = False
                    divided_query.append(last_word)
                    divided_query.append(next_block)
                    last_word = ""
                    next_block = ""
        else:  # add characters to next block until reaching a space or %
            next_block += char

    if len(divided_query) == 1:  # make sure single part queries are valid
        if not valid_commands.__contains__(divided_query[0]):
            divided_query.append("ERROR")
        else:
            if divided_query[0] is not "reload" and divided_query[0] is not "help" and divided_query[0] is not "exit":
                divided_query.append("ERROR")
    elif len(divided_query) == 2:  # there are no valid two part queries so this must be a mistake
        divided_query.append("ERROR")

    return divided_query


def print_help():
    # print all available commands
    print("help - prints all user commands")
    print("exit - quit the system")
    print("reload - reload the database")
    print("population state [x] - get the population for state [x]")
    print("population timezone [x] - get the population for timezone [x]")
    print("population city [x] (state [y]) - get the population for city [x]. you can also specify which state it's in, [y]")
    print("density city [x] (state [y]) - get the density for city [x]. you can also specify which state it's in, [y]")
    print("timezone city [x] (state [y]) - get the timezone for city [x]. you can also specify which state it's in, [y]")
    print("state city [x] - get the state or states with a city by that name in it.")
    print("capital state [x] - get the capital of the state.")

reinit_database()
run = True
success = False
while run:
    query = validate_and_split(raw_input("-> ") + "%")
    # start with checking if it's the three "basic" commands
    if query[0] == "exit":
        run = False
        success = True
    if query[0] == "help":
        success = True
        print_help()
    if query[0] == "reload":
        success = True
        reinit_database()
        print("Database reloaded")
    
    # if it got to this point, it's an actual query of the database
    if query[0] == "population":
        if query[1] == "timezone":  # population timezone [x]
            cur.execute("SELECT population FROM Cities WHERE timezone = ?", (query[2],))
            rows = cur.fetchall()
            if len(rows) > 0:
                timezone_pop = 0
                for row in rows:
                    if row[0] != -1:
                        timezone_pop += row[0]
                print(timezone_pop)
                success = True
            else:
                print "Your query returned no results"
        if query[1] == "state":  # population state [x]
            cur.execute("SELECT state_population FROM States WHERE state_name = ?", (query[2],))
            results = cur.fetchall()
            if len(results) > 0:
                print results[0]
                success = True
            else:
                print "Your query returned no results"
        if query[1] == "city":  # population city [x] (state x)
            try:
                check_if_exists = query[4]
                if query[3] == "state":
                    cur.execute("SELECT population FROM Cities WHERE state = ? AND city_name = ?", (query[4], query[2],))
                    results = cur.fetchall()
                    if len(results) > 0:
                        print results[0]
                        success = True
                    else:
                        print "Your query returned no results"

            except IndexError:  # index 3 doesnt exist, no state specified.
                cur.execute("SELECT * FROM Cities WHERE city_name = ?", (query[2],))
                rows = cur.fetchall()
                if len(rows) > 0:
                    for row in rows:
                        if row[2] == -1:
                            print("%s, %s: Population Unlisted in Database" % (query[2], row[1]))
                        else:
                            print("%s, %s: %s" % (query[2], row[1], row[2]))
                    success = True
                else:
                    print "Your query returned no results"
    elif query[0] == "density":  # density city x (state x)
        if query[1] == "city":
            try:
                check_if_exists = query[4]
                if query[3] == "state":
                    cur.execute("SELECT density FROM Cities WHERE state = ? AND city_name = ?", (query[4], query[2],))
                    results = cur.fetchall()
                    if len(results) > 0:
                        print results[0]
                        success = True
                    else:
                        print "Your query returned no results"

            except IndexError:  # index 3 doesnt exist, no state specified.
                cur.execute("SELECT * FROM Cities WHERE city_name = ?", (query[2],))
                rows = cur.fetchall()
                if len(rows) > 0:
                    for row in rows:
                        print("%s, %s: %s" % (query[2], row[1], row[3]))
                    success = True
                else:
                    print "Your query returned no results"
    elif query[0] == "timezone":  # timezone city x (state x)
        if query[1] == "city":
            try:
                check_if_exists = query[4]
                if query[3] == "state":
                    cur.execute("SELECT timezone FROM Cities WHERE state = ? AND city_name = ?", (query[4], query[2],))
                    results = cur.fetchall()
                    if len(results) > 0:
                        print results[0]
                        success = True
                    else:
                        print "Your query returned no results"

            except IndexError:  # index 3 doesnt exist, no state specified.
                cur.execute("SELECT * FROM Cities WHERE city_name = ?", (query[2],))
                rows = cur.fetchall()
                if len(rows) > 0:
                    for row in rows:
                        print("%s, %s: %s" % (query[2], row[1], row[4]))
                    success = True
                else:
                    print "Your query returned no results"
    elif query[0] == "state" and query[1] == "city":  # state city x
        cur.execute("SELECT state FROM Cities WHERE city_name = ?", (query[2],))
        rows = cur.fetchall()
        for row in rows:
            print("%s, %s" % (query[2], row[0]))
        success = True
    elif query[0] == "capital" and query[1] == "state":  # capital state [x]
        cur.execute("SELECT capital_city_id FROM States WHERE state_name = ?", (query[2],))
        try:
            capital_rowid = cur.fetchone()[0]
            cur.execute("SELECT city_name FROM Cities WHERE rowid = ?", (capital_rowid,))
            results = cur.fetchall()
            if len(results) > 0:
                print results[0]
            else:
                print "Your query returned no results"
        except TypeError:
            print "Your query returned no results"

    if not success:  # user failed to input a correct command, help them out
        if query:  # if list is empty this is false
            if query[0] == "population":
                print("Population commands: ")
                print("population state [x]")
                print("population timezone [x]")
                print("population city [x] (state [x])")
            if query[0] == "density":
                print("Density command: ")
                print("density city [x] (state [x])")
            if query[0] == "timezone":
                print("Timezone command: ")
                print("timezone city [x] (state [x])")
            if query[0] == "state":
                print("State command: ")
                print("state city [x]")
            if query[0] == "capital":
                print("Capital of state command: ")
                print("capital state [x]")
        
        print("\nYour query was unsuccessful. Make sure to properly capitalize state and city names,")
        print("as well as use proper names for timezones (ie, America/Denver).")
        print("The help command can show you how to structure valid commands.")
    success = False
