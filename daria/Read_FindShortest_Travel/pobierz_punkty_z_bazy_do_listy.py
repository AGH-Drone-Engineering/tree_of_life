#direct downloading from the database and storing in the 'latitude_longitude_list' list

import csv
from config import *
from firebase_admin import credentials, firestore, initialize_app

def download_points():
    db = firestore.client()

    # Retrieve all documents from the "tree-points" collection
    collection_ref = db.collection(collection_name)
    docs = collection_ref.stream()

    # Create a list to store all the data
    data = []
    latitude_longitude_color_list=[]
    for doc in docs:
        point = doc.to_dict()
        # print(point)
        latitude_longitude_color_list.append([point['location'].latitude, point['location'].longitude, point['type'], point['shooted']])
    print(latitude_longitude_color_list)
    # print(f"Data downloaded and stored in list 'latitude_longitude_color_list':")
    # print(latitude_longitude_color_list)
    return latitude_longitude_color_list
