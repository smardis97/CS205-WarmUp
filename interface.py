# population state [x]
# population timezone x
# population city [x] (state x)

# density city x (state x)

# timezone city x (state x)

# state city x

# exit
# help
# reload

from database import *


def print_help():
    # print all available commands
    print("help - prints all user commands")
    print("exit - quit the system")
    print("reload = reload the database")
    print("")

reinit_database()
run = True
success = False
while run:
    command = raw_input("-> ")
    # start with checking if it's the three "basic" commands
    if command == "exit":
        run = False
        success = True
    if command == "help":
        success = True
        print_help()
    if command == "reload":
        success = True
        reinit_database()
        print("Database reloaded")
    
    # if it got to this point, it's an actual query of the database
    query = command.split()
    if len(query) > 2:
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
                    print(rows)
                    for row in rows:
                        print("%s, %s: %s" % (query[2], row[1], row[2]))
                    success = True

        if query[0] == "density":  # density city x (state x)
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
                
        if query[0] == "timezone":  # timezone city x (state x)
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

        if query[0] == "state" and query[1] == "city":  # state city x
            cur.execute("SELECT state FROM Cities WHERE city_name = ?", (query[2],))
            print(cur.fetchone()[0])
            success = True

    # if not success: #user failed to input a correct command, help them out
