import sqlite3
#conn = sqlite3.connect('US_states')
import csv
Washington = 0
with open('US_Cities.csv') as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=',')
    line_count = 0
    for row in csv_reader:
        if line_count == 0:
            print(row[9])
            line_count +=1
        else:
            if row[3] == 'Washington' and row[8] != '':
                Washington += int(row[8])
            #print(row[0])
            #print(row[4])
            line_count += 1

print(Washington)
