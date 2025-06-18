from config import tickets_collection, technicians_collection
from datetime import datetime
from bson.objectid import ObjectId

def create_ticket(flat, issue_type, description, priority):
    ticket = {
        "flat": flat,
        "issue_type": issue_type,
        "description": description,
        "priority": priority,
        "status": "Open",
        "created_at": datetime.utcnow(),
        "assigned_to": None
    }
    tickets_collection.insert_one(ticket)

def get_all_tickets():
    return list(tickets_collection.find())

def get_open_tickets():
    return list(tickets_collection.find({"status": "Open"}))

def get_tickets_by_flat(flat):
    return list(tickets_collection.find({"flat": flat}))

def assign_ticket(ticket_id, technician_username):
    tickets_collection.update_one(
        {"_id": ObjectId(ticket_id)},
        {
            "$set": {
                "assigned_to": technician_username,
                "status": "In Progress",
                "assigned_at": datetime.utcnow()
            }
        }
    )

def close_ticket(ticket_id):
    tickets_collection.update_one(
        {"_id": ObjectId(ticket_id)},
        {"$set": {"status": "Resolved"}}
    )

def get_tickets_by_technician(technician_username):
    return list(tickets_collection.find({"assigned_to": technician_username}))

def get_technicians():
    return list(technicians_collection.find())

def add_technician(username, mobile):
    technicians_collection.insert_one({"username": username, "mobile": mobile})
