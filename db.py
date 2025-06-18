# db.py
from config import ticket_collection, technician_collection, user_collection
from bson.objectid import ObjectId
from datetime import datetime

def create_ticket(name, flat, issue_type, description):
    ticket = {
        "name": name,
        "flat": flat,
        "issue_type": issue_type,
        "description": description,
        "status": "Open",
        "created_at": datetime.utcnow(),
        "priority": None,
        "assigned_to": None
    }
    ticket_collection.insert_one(ticket)

def get_all_tickets():
    return list(ticket_collection.find())

def get_tickets_by_user(name, flat):
    return list(ticket_collection.find({"name": name, "flat": flat}))

def get_technicians():
    return list(technician_collection.find())

def assign_ticket(ticket_id, technician_id, priority):
    technician = technician_collection.find_one({"_id": ObjectId(technician_id)})
    if technician:
        ticket_collection.update_one(
            {"_id": ObjectId(ticket_id)},
            {
                "$set": {
                    "assigned_to": {
                        "id": str(technician["_id"]),
                        "name": technician["name"],
                        "mobile": technician["mobile"]
                    },
                    "status": "In Progress",
                    "priority": priority,
                    "assigned_at": datetime.utcnow()
                }
            }
        )

def add_technician(name, mobile, username, password):
    technician_collection.insert_one({
        "name": name,
        "mobile": mobile,
        "username": username,
        "password": password
    })

def authenticate_technician(username, password):
    return technician_collection.find_one({"username": username, "password": password})

def get_technician_tickets(tech_id):
    return list(ticket_collection.find({"assigned_to.id": tech_id}))

def update_ticket_status(ticket_id, status):
    ticket_collection.update_one(
        {"_id": ObjectId(ticket_id)},
        {"$set": {"status": status, "updated_at": datetime.utcnow()}}
    )
