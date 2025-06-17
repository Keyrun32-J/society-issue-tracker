# db.py
from config import ticket_collection
from datetime import datetime
from bson.objectid import ObjectId

def create_ticket(flat, issue_type, desc, raised_by):
    ticket = {
        "flat_number": flat,
        "issue_type": issue_type,
        "description": desc,
        "raised_by": raised_by,
        "status": "Open",
        "assigned_to": "",
        "created_at": datetime.now(),
        "updated_at": datetime.now()
    }
    ticket_collection.insert_one(ticket)

def get_all_tickets():
    return list(ticket_collection.find())

def assign_ticket(ticket_id, assignee):
    ticket_collection.update_one(
        {"_id": ObjectId(ticket_id)},
        {"$set": {"assigned_to": assignee, "status": "In Progress", "updated_at": datetime.now()}}
    )

def close_ticket(ticket_id):
    ticket_collection.update_one(
        {"_id": ObjectId(ticket_id)},
        {"$set": {"status": "Closed", "updated_at": datetime.now()}}
    )
