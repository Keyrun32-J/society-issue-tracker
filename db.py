# FILE: db.py
from config import ticket_collection, user_collection

def create_ticket(title, description, mobile):
    ticket = {
        "title": title,
        "description": description,
        "status": "Open",
        "assigned_to": None,
        "mobile": mobile  # ← Add this line
    }
    ticket_collection.insert_one(ticket)


def get_all_tickets():
    return list(ticket_collection.find())

def assign_ticket(ticket_id, technician_username):
    technician = user_collection.find_one({"username": technician_username})
    if technician:
        ticket_collection.update_one(
            {"_id": ticket_id},
            {"$set": {
                "assigned_to": technician["username"],
                "mobile": technician["mobile"],
                "status": "Assigned"
            }}
        )

def close_ticket(ticket_id):
    ticket_collection.update_one(
        {"_id": ticket_id},
        {"$set": {"status": "Closed"}}
    )

def get_all_technicians():
    return list(user_collection.find())
