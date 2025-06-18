# db.py
from pymongo import MongoClient
from datetime import datetime
from bson.objectid import ObjectId

# --- MongoDB Setup ---
client = MongoClient("mongodb://localhost:27017")  # Or use MongoDB Atlas URI
db = client["society_issue_tracker"]

tickets = db["tickets"]
technicians = db["technicians"]

# --- DB Functions ---
def create_ticket(flat_no, issue_type, description):
    ticket = {
        "flat_no": flat_no,
        "issue_type": issue_type,
        "description": description,
        "status": "Pending",
        "created_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "assigned_to": None,
        "priority": None,
        "raised_by": "resident"
    }
    tickets.insert_one(ticket)

def get_all_tickets():
    return list(tickets.find())

def get_open_tickets():
    return list(tickets.find({"assigned_to": None}))

def assign_ticket(ticket_id, technician_username, priority):
    tickets.update_one(
        {"_id": ObjectId(ticket_id)},
        {"$set": {
            "assigned_to": technician_username,
            "priority": priority,
            "status": "In Progress"
        }}
    )

def update_ticket_status(ticket_id, new_status):
    tickets.update_one(
        {"_id": ObjectId(ticket_id)},
        {"$set": {"status": new_status}}
    )

def get_technicians():
    return list(technicians.find())

def get_tickets_by_resident(username):
    return list(tickets.find({"raised_by": username}))

def get_tickets_by_technician(username):
    return list(tickets.find({"assigned_to": username}))
