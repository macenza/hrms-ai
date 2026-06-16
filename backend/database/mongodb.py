from pymongo import MongoClient

client = MongoClient("mongodb://localhost:27017")

db = client["hrms"]

application_collection = db["applications"]