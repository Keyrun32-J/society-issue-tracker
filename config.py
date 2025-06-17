# config.py
from pymongo import MongoClient

# Replace this with your actual MongoDB URI
MONGO_URI = "mongodb+srv://society_user:Bank%401980@cluster0.sy8c2a5.mongodb.net/?retryWrites=true&w=majority"

client = MongoClient(MONGO_URI)
db = client["society_issue_db"]
ticket_collection = db["tickets"]

# Predefined technicians dictionary
technicians = {
    "tech_1": {"name": "Ravi Kumar", "mobile": "9876543210"},
    "tech_2": {"name": "Amit Sharma", "mobile": "9876543211"},
    "tech_3": {"name": "Vijay Patil", "mobile": "9876543212"},
    "tech_4": {"name": "Sunil Joshi", "mobile": "9876543213"},
    "tech_5": {"name": "Ramesh Desai", "mobile": "9876543214"},
    "tech_6": {"name": "Karan Mehta", "mobile": "9876543215"},
}
