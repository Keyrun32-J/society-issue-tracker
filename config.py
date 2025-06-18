# config.py
from pymongo import MongoClient

# Hardcoded MongoDB URI for now (you can store in .env in production)
MONGO_URI = "mongodb+srv://society_user:Bank%401980@cluster0.sy8c2a5.mongodb.net/?retryWrites=true&w=majority"

client = MongoClient(MONGO_URI)
db = client["society"]

ticket_collection = db["tickets"]
technician_collection = db["technicians"]
user_collection = db["users"]