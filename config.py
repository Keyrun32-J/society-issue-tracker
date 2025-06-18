# config.py
from pymongo import MongoClient
import os

# Use your actual Mongo URI here or set it as environment variable
MONGO_URI = os.getenv("MONGO_URI", "mongodb+srv://society_user:Bank%401980@cluster0.sy8c2a5.mongodb.net/?retryWrites=true&w=majority")

client = MongoClient(MONGO_URI)
db = client["society"]

# Collections
ticket_collection = db["tickets"]
technician_collection = db["technicians"]
user_collection = db["users"]
