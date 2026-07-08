from pymongo import MongoClient
import os
from dotenv import load_dotenv

load_dotenv()

mongo_uri = os.getenv("MONGO_URI", "mongodb+srv://macenza:macenza1234@cluster0.z50jiib.mongodb.net/?appName=Cluster0")
client = MongoClient(mongo_uri)

db = client["hrms"]

application_collection = db["applications"]