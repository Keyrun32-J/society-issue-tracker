# config.py
from pymongo import MongoClient

# MongoDB connection string
MONGO_URI = "mongodb+srv://society_user:Bank%401980@cluster0.sy8c2a5.mongodb.net/"

client = MongoClient(MONGO_URI)
db = client["society_db"]
ticket_collection = db["tickets"]
