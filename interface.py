#population state [x]

#population city [x] (state x)
#density city x (state x)
#timezone city x (state x)

#state city x
#population timezone x

#exit
#help
#reload

from database import *

def print_help():
    #print all available commands
    print("help - prints all user commands")
    print("exit - quit the system")
    print("reload = reload the database")
    print("")

run = True
success = False
while (run):
    command = raw_input(">>")
    #start with checking if it's the three "basic" commands
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
    
    #if it got to this point, it's an actual query of the database
    query = command.split()
    query.reverse() #what we're looking for will be index 0 followed by tokens
    if query[1] == "state":
        if query[2] == "population": #population state [x]
            #select row that is the correct state
            cur.execute("SELECT state_population FROM States WHERE state_name = ?", (query[0]))
            row = cur.fetchAll()
            row.split()
            print(row[2])
            success = True

        #population city [x] (state x)
        #density city x (state x)
        #timezone city x (state x)
        if query[3] == "city":
            pass
            
        
    if query[1] == "city":
        pass
        #command could be:
        #population city [x] (state x)
        #density city x (state x)
        #timezone city x (state x)
        #state city x
    if query[1] == "timezone":
        pass
        #add all population of timezone and print

    if not success:
        pass
        #user failed to input a correct command, help them out
