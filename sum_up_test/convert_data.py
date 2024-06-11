import csv
from datetime import datetime
import os

#This script is to format data from store and transaction, files csv
#to handle data associate to date/ datetime, after excute this script
#data will be able to be carge into the corresponding tables, 
#if you try to load the data before this an error is gotten.

def convert_date(date_str):
    old_format = "%m/%d/%Y %H:%M:%S"
    new_format = "%Y-%m-%d %H:%M:%S"
    return datetime.strptime(date_str, old_format).strftime(new_format)


file_path = 'store.csv'
temp_file_path = 'temp.csv'

with open(file_path, 'r') as csvfile:
    reader = csv.reader(csvfile)
    header = next(reader)

    rows = []
    for row in reader:
        created_at = convert_date(row[5])
        row[5] = created_at
        rows.append(row)

with open(temp_file_path, 'w', newline='') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(header)
    writer.writerows(rows)


os.replace(temp_file_path, file_path)


file_path = 'transaction.csv'
temp_file_path = 'temp.csv'

with open(file_path, 'r') as csvfile:
    reader = csv.reader(csvfile)
    header = next(reader)

    rows = []
    for row in reader:
        created_at = convert_date(row[9])
        happened_at = convert_date(row[10])
        row[9] = created_at
        row[10] = happened_at
        rows.append(row)

with open(temp_file_path, 'w', newline='') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(header)
    writer.writerows(rows)

os.replace(temp_file_path, file_path)
