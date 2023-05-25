import csv
from config import *
from firebase_admin import credentials, firestore

def add_points_to_database():
    db = firestore.client()

    # Define the CSV file path
    # csv_file = "tree_points.csv"

    # Define the CSV headers based on the document properties
    headers = ["img", "location", "name", "shooted", "timestamp", "type"]

    # Read the data from the CSV file

    is_shooted="false"
    my_data=[[0., 0.,"white", is_shooted], [7,3, "brown", is_shooted], [1,5,"brown", is_shooted], [2.5,4,"gold", is_shooted], [10,10,"brown", is_shooted], [2,0.7,"white", is_shooted], [1.2, 5,"white", is_shooted], [2.9, 4,"white", is_shooted], [3.5,4,"white", is_shooted], [9, 6.7,"white", is_shooted], [9, 8.8,"white", is_shooted]]

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
        row['type'] = my_data[i][2]
        row['shooted'] = "false" #row['shooted'].lower() == 'true'
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

if __name__ == "__main__":
    add_points_to_database()