# config.py
from pymongo import MongoClient

MONGO_URI = "mongodb+srv://society_user:Bank%401980@cluster0.sy8c2a5.mongodb.net/?retryWrites=true&w=majority"

client = MongoClient(MONGO_URI)
db = client["society"]
ticket_collection = db["tickets"]
technician_collection = db["technicians"]
user_collection = db["users"]
