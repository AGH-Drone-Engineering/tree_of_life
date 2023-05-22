#direct downloading from the database and storing in the 'latitude_longitude_list' list

import csv
from config import *
from firebase_admin import credentials, firestore, initialize_app
import rospy

db = firestore.client()


def points_targets_finished_mission() -> list[list]:
    # Retrieve all documents from the "tree-points" collection
    collection_ref = db.collection(collection_name)
    docs = collection_ref.stream()


    # Create a list to store all the data
    data = []
    latitude_longitude_list=[]
    for doc in docs:
        point = doc.to_dict()
        latitude_longitude_list.append([point['location'].latitude, point['location'].longitude])
    rospy.loginfo("Data downloaded and stored in list 'latitude_longitude_list':")
    rospy.logifno(str(latitude_longitude_list))

    return latitude_longitude_list
