from firebase_admin import firestore
from config import *
from datetime import datetime, timezone


def update_firestore_document(latitude, longitude, altitude=0, heading=0, velocity=0):

    '''
    This function is to publicate data from robo-dog
    '''
    # Create a Firestore client
    db = firestore.client()
    collection = db.collection("dog-data")
    query = collection.limit(1)
    # Get the first document from the query results
    documents = query.get()
    first_document = next(iter(documents))
    # Get the reference to the document
    doc_ref = collection.document(first_document.id)
    # Update the document with the given fields
    doc_ref.update({ 'location': firestore.GeoPoint(latitude, longitude), 'altitude': altitude, 'heading': heading, 'velocity':velocity })




def points_targets_finished_mission():
    '''
    this function gives list of list with points 
    '''
    db = firestore.client()
    # Retrieve all documents from the "tree-points" collection
    collection_ref = db.collection(collection_name)
    docs = collection_ref.stream()


    # Create a list to store all the data
    data = []
    latitude_longitude_list=[]
    for doc in docs:
        point = doc.to_dict()
        latitude_longitude_list.append([point['location'].latitude, point['location'].longitude])
    print("Data downloaded and stored in list 'latitude_longitude_list':")
    print(latitude_longitude_list)

    return latitude_longitude_list

def get_drone_data():
  # Initialize the Firebase app
  cred = credentials.Certificate('key.json')
  db = firestore.client()
  # Reference the "drone-path" collection in Firestore
  collection_ref = db.collection('drone-path')
  # Query the Firestore collection to get the newest point based on timestamp field
  query = collection_ref.order_by('timestamp', direction=firestore.Query.DESCENDING).limit(1)
  results = query.get()
  # Extract the location and altitude values from the retrieved point
  return results[0]



def is_drone_on_ground():

    """
    This function gives information about status of drone mission 
    if 0 - drone continues mission 
    else: dog can start its mission
    """
    def get_drone_alt():
        return get_drone_data().get("altitude")

    def get_drone_lasttime():
        timestamp = get_drone_data().get("timestamp")
        timestamp = timestamp.replace(tzinfo=timezone.utc).astimezone(timezone.utc)
        current_time = datetime.now(timezone.utc)
        time_diff = (current_time - timestamp).total_seconds()
        return time_diff
    
    return get_drone_alt() < 0.5 or get_drone_lasttime() >= 8



