import csv
from config import *
from firebase_admin import credentials, firestore, initialize_app

db = firestore.client()

# Retrieve all documents from the "tree-points" collection
collection_ref = db.collection(collection_name)
docs = collection_ref.stream()

# Create a list to store all the data
data = []
for doc in docs:
    point = doc.to_dict()
    point['location'] = [point['location'].latitude, point['location'].longitude]
    data.append(point)

# Define the CSV file path
csv_file = "tree_points.csv"

# Define the CSV headers based on the document properties
headers = ["img", "location", "name", "shooted", "timestamp", "type"]

# Write the data to the CSV file
with open(csv_file, mode="w", newline="") as file:
    writer = csv.DictWriter(file, fieldnames=headers)
    writer.writeheader()
    writer.writerows(data)

print(f"Data downloaded and saved as {csv_file}")
