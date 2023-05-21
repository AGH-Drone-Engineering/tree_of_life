import csv
from config import *
from firebase_admin import credentials, firestore

db = firestore.client()

# Define the CSV file path
# csv_file = "tree_points.csv"

# Define the CSV headers based on the document properties
headers = ["img", "location", "name", "shooted", "timestamp", "type"]

# Read the data from the CSV file

my_data=[[1,1],[2,2],[4,5],[6,7]]
data = []
# with open(csv_file, mode="r") as file:
#     reader = csv.DictReader(file)
#     for row in reader:
        # Convert the 'location' field to a GeoPoint
        # coordinates = row['location'].split(',')
        # latitude = float(coordinates[0][1].strip())
        # longitude = float(coordinates[1][:-1].strip())
        # row['location'] = firestore.GeoPoint(latitude, longitude)
        # row['timestamp'] = firestore.SERVER_TIMESTAMP
        # row['shooted'] = row['shooted'].lower() == 'true'
        # data.append(dict(row))
for i in range(len(my_data)):
    row=dict()
    # nates = row['location'].split(',')
    latitude = float(my_data[i][0])
    longitude = float(my_data[i][1])
    row['location'] = firestore.GeoPoint(latitude, longitude)
    row['timestamp'] = firestore.SERVER_TIMESTAMP
    row['shooted'] = "true" #row['shooted'].lower() == 'true'
    data.append(dict(row))
# Verify CSV compatibility by checking if headers match
# if reader.fieldnames != headers:
#     print("CSV file is not compatible with the model. Aborting.")
#     exit()

# Upload records from the CSV file to Firebase
collection_ref = db.collection(collection_name)
for item in data:
    collection_ref.add(item)

print("Data uploaded to Firebase successfully.")
