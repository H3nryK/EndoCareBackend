import firebase_admin
from firebase_admin import credentials, auth
import os

# Load Firebase credentials
cred_file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "firebase-credentials.json")
cred = credentials.Certificate(cred_file_path)
firebase_admin.initialize_app(cred)
