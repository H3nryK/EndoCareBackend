import firebase_admin
from firebase_admin import credentials, auth

# Load Firebase credentials
cred = credentials.Certificate("firebase-credentials.json")
firebase_admin.initialize_app(cred)
