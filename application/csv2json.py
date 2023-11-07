import csv
import sys
import json
import os

# Creates a new csv file named 'edited_csv' that doesn't contain empty rows, or rows with empty fields
def csv_cleanup(csvfilename):
    with open(csvfilename, newline='') as csvfile:
        with open('edited_csv', 'w', newline='') as edited_csvfile:
            original = csv.reader(csvfile, delimiter=';')
            edited = csv.writer(edited_csvfile, delimiter=';')
            # fieldnames = next(original)
            # fieldnames.insert(0, "#")
            # edited.writerow(fieldnames)
            # i = 1
            for row in original:
                if row and any(row) and any(field.strip() for field in row):
                    # row.insert(0, i)
                    edited.writerow(row)
                    # i += 1

# Creates a json file from the edited csv file with an incremental integer as keys
def csv_to_json(filename):
    data_dict = {}
    with open('edited_csv', newline='') as csvfile:
        edited = csv.DictReader(csvfile, delimiter=';')
        key = 1
        for row in edited: 
            data_dict[key] = row
            key += 1
    with open(filename+'.json', 'w') as jsonfile:
        jsonfile.write(json.dumps(data_dict, indent = 4))



csvfilename = sys.argv[1]
filename = csvfilename.split('/')[-1].split('.')[0]

csv_cleanup(csvfilename)
csv_to_json(filename)
os.remove('edited_csv')



        