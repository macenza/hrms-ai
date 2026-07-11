import os
import urllib.parse
from pymongo import MongoClient
from dotenv import load_dotenv

load_dotenv()

mongo_uri = os.getenv("MONGO_URI") or "mongodb://localhost:27017"
client = MongoClient(mongo_uri)

db_name = "test"
try:
    parsed_uri = urllib.parse.urlparse(mongo_uri)
    path = parsed_uri.path
    if path and path.strip("/"):
        db_name = path.strip("/").split("?")[0]
except:
    pass

db = client[db_name]

application_collection = db["applications"]
