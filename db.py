from config import ticket_collection, technician_collection, user_collection
from bson.objectid import ObjectId

# --- Ticket Operations ---
def create_ticket(ticket):
    ticket_collection.insert_one(ticket)

def get_all_tickets():
    return list(ticket_collection.find())

def get_tickets_by_user(flat_number):
    return list(ticket_collection.find({"flat": flat_number}))

def assign_ticket_to_technician(ticket_id, technician_name, priority, status="In Progress"):
    ticket_collection.update_one(
        {"_id": ObjectId(ticket_id)},
        {"$set": {
            "assigned_to": technician_name,
            "priority": priority,
            "status": status
        }}
    )

def get_tickets_by_technician(technician_name):
    return list(ticket_collection.find({"assigned_to": technician_name}))

# --- Technician Operations ---
def add_technician(name, mobile):
    technician_collection.insert_one({"name": name, "mobile": mobile})

def get_technicians():
    return list(technician_collection.find())
