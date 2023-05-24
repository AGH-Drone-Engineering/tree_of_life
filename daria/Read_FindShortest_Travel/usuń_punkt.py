from config import *
from firebase_admin import credentials, firestore

db = firestore.client()

# Clear the "tree-points" collection
collection_ref = db.collection(collection_name)
docs = collection_ref.stream()

for doc in docs:
    doc.reference.delete()

print("Collection cleared successfully.")
