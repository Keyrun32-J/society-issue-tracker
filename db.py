# db.py
from config import ticket_collection, technician_collection, user_collection
from bson.objectid import ObjectId

def create_ticket(flat, issue_type, description):
    ticket_collection.insert_one({
        "flat": flat,
        "issue_type": issue_type,
        "description": description,
        "status": "Open"
    })

def get_all_tickets():
    return list(ticket_collection.find())

def get_tickets_by_user(username):
    return list(ticket_collection.find({"flat": username}))

def assign_ticket(ticket_id, technician_username, priority):
    ticket_collection.update_one(
        {"_id": ObjectId(ticket_id)},
        {"$set": {
            "technician": technician_username,
            "priority": priority,
            "status": "Assigned"
        }}
    )

def update_ticket_status(ticket_id, status):
    ticket_collection.update_one({"_id": ObjectId(ticket_id)}, {"$set": {"status": status}})

def create_user(username, password):
    if not user_collection.find_one({"username": username}):
        user_collection.insert_one({"username": username, "password": password})

def create_technician(name, mobile, username, password):
    if not technician_collection.find_one({"username": username}):
        technician_collection.insert_one({
            "name": name,
            "mobile": mobile,
            "username": username,
            "password": password
        })

def get_technicians():
    return list(technician_collection.find())

def authenticate_user(username, password, user_type="resident"):
    collection = user_collection if user_type == "resident" else technician_collection
    return collection.find_one({"username": username, "password": password})

def get_tickets_by_technician(technician_username):
    return list(ticket_collection.find({"technician": technician_username}))
