# config.py
from pymongo import MongoClient

# MongoDB connection string
client = MongoClient("mongodb+srv://society_user:Bank@1980@cluster0.sy8c2a5.mongodb.net/")  # or your Mongo URI

client = MongoClient(MONGO_URI)
db = client["society_db"]
ticket_collection = db["tickets"]
