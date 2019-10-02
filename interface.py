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


def validate_and_split(query):
    divided_query = []
    next_block = ""
    last_word = ""
    multi_word = False
    for char in query:
        if char == " ":
            if not multi_word:
                if not valid_commands.__contains__(next_block):
                    multi_word = True
                    last_word = next_block
                    next_block = ""
                else:
                    divided_query.append(next_block)
                    next_block = ""
            else:
                if not valid_commands.__contains__(next_block):
                    last_word += " " + next_block
                    next_block = ""
                else:
                    multi_word = False
                    divided_query.append(last_word)
                    divided_query.append(next_block)
                    last_word = ""
                    next_block = ""
        elif char == "%":
            if not multi_word:
                divided_query.append(next_block)
                next_block = ""
            else:
                last_word += " " + next_block
                next_block = ""
                divided_query.append(last_word)
                last_word = ""
        else:
            next_block += char

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

reinit_database()
run = True
success = False
while run:
    query = validate_and_split(raw_input("-> ") + "%")
    # start with checking if it's the three "basic" commands
    if query == "exit":
        run = False
        success = True
    if query == "help":
        success = True
        print_help()
    if query == "reload":
        success = True
        reinit_database()
        print("Database reloaded")
    
    # if it got to this point, it's an actual query of the database
    if query[0] == "population":
            if query[1] == "timezone":  # population timezone [x]
                cur.execute("SELECT population FROM Cities WHERE timezone = ?", (query[2],))
                rows = cur.fetchall()
                timezone_pop = 0
                for row in rows:
                    if row[0] != -1:
                        timezone_pop += row[0]
                print(timezone_pop)
                success = True
            if query[1] == "state":  # population state [x]
                cur.execute("SELECT state_population FROM States WHERE state_name = ?", (query[2],))
                print(cur.fetchone()[0])
                success = True
            if query[1] == "city":  # population city [x] (state x)
                try:
                    check_if_exists = query[4]
                    if query[3] == "state":
                        cur.execute("SELECT population FROM Cities WHERE state = ? AND city_name = ?", (query[4], query[2],))
                        print(cur.fetchone()[0])
                        success = True
                except IndexError:  # index 3 doesnt exist, no state specified.
                    cur.execute("SELECT * FROM Cities WHERE city_name = ?", (query[2],))
                    rows = cur.fetchall()
                    for row in rows:
                        if row[2] == -1:
                            print("%s, %s: Population Unlisted in Database" % (query[2], row[1]))
                        else:
                            print("%s, %s: %s" % (query[2], row[1], row[2]))
                    success = True
        
    elif query[0] == "density": # density city x (state x)
        if query[1] == "city":
            try:
                check_if_exists = query[4]
                if query[3] == "state":
                    cur.execute("SELECT density FROM Cities WHERE state = ? AND city_name = ?", (query[4], query[2],))
                    print(cur.fetchone()[0])
                    success = True
            except IndexError:  # index 3 doesnt exist, no state specified.
                cur.execute("SELECT * FROM Cities WHERE city_name = ?", (query[2],))
                rows = cur.fetchall()
                for row in rows:
                    print("%s, %s: %s" % (query[2], row[1], row[3]))
                success = True
    elif query[0] == "timezone":  # timezone city x (state x)
        if query[1] == "city":
            try:
                check_if_exists = query[4]
                if query[3] == "state":
                    cur.execute("SELECT timezone FROM Cities WHERE state = ? AND city_name = ?", (query[4], query[2],))
                    print(cur.fetchone()[0])
                    success = True
            except IndexError:  # index 3 doesnt exist, no state specified.
                cur.execute("SELECT * FROM Cities WHERE city_name = ?", (query[2],))
                rows = cur.fetchall()
                for row in rows:
                    print("%s, %s: %s" % (query[2], row[1], row[4]))
                success = True
    elif query[0] == "state" and query[1] == "city":  # state city x
        cur.execute("SELECT state FROM Cities WHERE city_name = ?", (query[2],))
        rows = cur.fetchall()
        for row in rows:
            print("%s, %s" % (query[2], row[0]))
        success = True
    elif query[0] == "capital" and query[1] == "state":  # capital state [x]
        cur.execute("SELECT capital_city_id FROM States WHERE state_name = ?", (query[2],))
        capital_rowid = cur.fetchone()[0]
        cur.execute("SELECT city_name FROM Cities WHERE rowid = ?", (capital_rowid,))
        print(cur.fetchone()[0])

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
        
        print("\nYour query was unsuccessful. Make sure to properly capitalize state and "
              "city names, as well as use proper names for timezones (ie, America/Denver)."
              " The help command can show you how to structure valid commands.")
    success = False
