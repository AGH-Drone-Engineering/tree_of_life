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
data_readable=[]
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
        # print(latitude, ',', longitude, ',', row["shooted"])
        tmp_dict['latitude']=latitude
        tmp_dict['longitude']=longitude
        tmp_dict["shooted"]=row["shooted"]
        data_readable.append(tmp_dict)

for tmp_dict in data_readable:   
    # latitude, longitude, shooted from tmp_dict
    for x in tmp_dict:
        print(tmp_dict[x], end=', ')
    print()

# Verify CSV compatibility by checking if headers match
if reader.fieldnames != headers:
    print("CSV file is not compatible with the model. Aborting.")
    exit()

# # Upload records from the CSV file to Firebase
# collection_ref = db.collection(collection_name)
# for item in data:
#     collection_ref.add(item)

# print("Data uploaded to Firebase successfully.")
