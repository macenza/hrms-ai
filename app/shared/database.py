import os
import urllib.parse
from pymongo import MongoClient
from dotenv import load_dotenv

load_dotenv(override=True)

_client = None
_db = None

def get_db():
    global _client, _db
    if _db is None:
        mongo_uri = os.getenv("MONGO_URI")
        if not mongo_uri or mongo_uri.strip() == "":
            raise ValueError("MONGO_URI is not defined in hrms-ai/.env or environment variables. Please check your configuration.")
        _client = MongoClient(mongo_uri)
        
        db_name = "hrms"
        try:
            parsed_uri = urllib.parse.urlparse(mongo_uri)
            path = parsed_uri.path
            if path and path.strip("/"):
                db_name = path.strip("/").split("?")[0]
        except:
            pass
        _db = _client[db_name]
    return _db

class DatabaseProxy:
    def __getitem__(self, collection_name):
        return get_db()[collection_name]
        
    def __getattr__(self, collection_name):
        return get_db()[collection_name]

db = DatabaseProxy()

# Wrap application_collection lazily to avoid database call at startup
class CollectionProxy:
    def __init__(self, collection_name):
        self._name = collection_name
        
    def _get_collection(self):
        return db[self._name]
        
    def __getattr__(self, name):
        return getattr(self._get_collection(), name)

application_collection = CollectionProxy("applications")
