import os
import json
import firebase_admin
from firebase_admin import credentials
from django.conf import settings

def initialize_firebase():
    try:
        firebase_admin.get_app()
    except ValueError:
        # Try to get credentials from environment variable first
        firebase_creds = os.getenv('FIREBASE_CREDENTIALS')
        
        if firebase_creds:
            # If credentials are provided as a JSON string in environment variable
            try:
                cred_dict = json.loads(firebase_creds)
                cred = credentials.Certificate(cred_dict)
            except json.JSONDecodeError:
                raise ValueError("Invalid FIREBASE_CREDENTIALS environment variable")
        else:
            # Fall back to file-based credentials
            cred_path = os.getenv(
                'FIREBASE_CREDENTIALS_PATH',
                os.path.join(settings.BASE_DIR, 'core', 'firebase-credentials.json')
            )
            
            if not os.path.exists(cred_path):
                raise FileNotFoundError(
                    "Firebase credentials not found. Either set FIREBASE_CREDENTIALS "
                    "environment variable with the JSON credentials or place the "
                    f"credentials file at: {cred_path}"
                )
            
            cred = credentials.Certificate(cred_path)
        
        firebase_admin.initialize_app(cred)