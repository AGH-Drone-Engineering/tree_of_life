import firebase_admin
from firebase_admin import credentials

# Firebase configuration
DATABASE_URL = "https://droniada-test-2023.firebaseio.com"
SERVICE_ACCOUNT_KEY = "key.json"

# DB config
# collection_name = "tree-points"
collection_name = "lots-of-points"

# Initialize Firebase Admin SDK
cred = credentials.Certificate(SERVICE_ACCOUNT_KEY)
firebase_admin.initialize_app(cred, {"databaseURL": DATABASE_URL})
