from pymongo import MongoClient
from bson.objectid import ObjectId
import os

# Load MongoDB URI from environment or use default
MONGO_URI = os.getenv(
    "MONGO_URI",
    "mongodb+srv://society_user:Bank%401980@cluster0.sy8c2a5.mongodb.net/?retryWrites=true&w=majority"
)

# Initialize MongoDB connection
client = MongoClient(MONGO_URI)
db = client["society"]

# Collections
ticket_collection = db["tickets"]
technician_collection = db["technicians"]
user_collection = db["users"]

# ------------------- FUNCTIONS ------------------- #

# Create a new ticket
def create_ticket(ticket):
    ticket_collection.insert_one(ticket)

# Get all tickets
def get_all_tickets():
    return list(ticket_collection.find())

# Get tickets by resident flat number
def get_tickets_by_user(flat_number):
    return list(ticket_collection.find({"flat": flat_number}))

# Assign ticket to technician and set priority/status
def assign_ticket_to_technician(ticket_id, technician_name, priority, status="In Progress"):
    if not isinstance(ticket_id, ObjectId):
        try:
            ticket_id = ObjectId(ticket_id)
        except Exception:
            return
    ticket_collection.update_one(
        {"_id": ticket_id},
        {"$set": {
            "assigned_to": technician_name,
            "priority": priority,
            "status": status
        }}
    )

# Add a new technician
def add_technician(name, mobile):
    technician_collection.insert_one({"name": name, "mobile": mobile})

# Get all technicians
def get_technicians():
    return list(technician_collection.find())

# Get tickets assigned to a specific technician
def get_tickets_by_technician(technician_name):
    return list(ticket_collection.find({"assigned_to": technician_name}))
