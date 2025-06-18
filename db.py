from config import ticket_collection, technician_collection, user_collection
from datetime import datetime
from bson import ObjectId


def create_ticket(flat_no, issue_type, description):
    ticket = {
        "flat_no": flat_no,
        "issue_type": issue_type,
        "description": description,
        "status": "Open",
        "priority": None,
        "assigned_to": None,
        "created_at": datetime.utcnow()
    }
    ticket_collection.insert_one(ticket)


def get_tickets_by_flat(flat_no):
    return list(ticket_collection.find({"flat_no": flat_no}))


def get_all_tickets():
    return list(ticket_collection.find())


def get_open_tickets():
    return list(ticket_collection.find({"status": "Open"}))


def assign_ticket(ticket_id, technician_username, priority):
    ticket_collection.update_one(
        {"_id": ObjectId(ticket_id)},
        {
            "$set": {
                "assigned_to": technician_username,
                "priority": priority,
                "status": "In Progress"
            }
        }
    )


def close_ticket(ticket_id):
    ticket_collection.update_one(
        {"_id": ObjectId(ticket_id)},
        {"$set": {"status": "Closed"}}
    )


def get_technician_tickets(tech_username):
    return list(ticket_collection.find({"assigned_to": tech_username}))


def add_technician(username, name, mobile):
    technician_collection.insert_one({
        "username": username,
        "name": name,
        "mobile": mobile
    })


def get_all_technicians():
    return list(technician_collection.find())


def get_technician_details(username):
    return technician_collection.find_one({"username": username})


def authenticate_user(username, role):
    if role == "resident":
        return True  # Simplified: all residents are allowed
    elif role == "manager":
        return username == "manager"
    elif role == "technician":
        return technician_collection.find_one({"username": username}) is not None
    return False
