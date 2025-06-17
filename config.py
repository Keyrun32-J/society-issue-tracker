# config.py
from pymongo import MongoClient

# MongoDB connection string
client = MongoClient("mongodb+srv://society_user:<db_password>@cluster0.sy8c2a5.mongodb.net/")  # or your Mongo URI

db = client["society_db"]
ticket_collection = db["tickets"]
