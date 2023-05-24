from firebase_admin import firestore
from config import *

def update_firestore_document(latitude, longitude, altitude=0, heading=0, velocity=0):
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

