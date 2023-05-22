#reading data from csv, storing in 'latitude_longitude_list' and printing

import csv
from config import *
from firebase_admin import credentials, firestore

db = firestore.client()

# Define the CSV file path
csv_file = "tree_points.csv"

# Define the CSV headers based on the document properties
headers = ["img", "location", "name", "shooted", "timestamp", "type"]

# Read the data from the CSV file
data = []
latitude_longitude_list=[]
with open(csv_file, mode="r") as file:
    reader = csv.DictReader(file)
    for row in reader:
        tmp_dict=dict()
        # Convert the 'location' field to a GeoPoint
        coordinates = row['location'].split(',')
        latitude = float(coordinates[0][1].strip())
        longitude = float(coordinates[1][:-1].strip())
        row['location'] = firestore.GeoPoint(latitude, longitude)
        row['timestamp'] = firestore.SERVER_TIMESTAMP
        row['shooted'] = row['shooted'].lower() == 'true'
        data.append(dict(row))
        latitude_longitude_list.append([latitude, longitude])

print(latitude_longitude_list)

print("Data read from Firebase successfully.")
