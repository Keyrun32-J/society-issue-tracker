# db.py
from config import ticket_collection, technicians

def create_ticket(flat_number, issue_type, description):
    ticket = {
        "flat_number": flat_number,
        "issue_type": issue_type,
        "description": description,
        "status": "Open",
        "assigned_to": None
    }
    ticket_collection.insert_one(ticket)

def get_all_tickets():
    return list(ticket_collection.find())

def assign_ticket(ticket_id, technician_id):
    technician = technicians.get(technician_id)
    if technician:
        ticket_collection.update_one(
            {"_id": ticket_id},
            {"$set": {
                "assigned_to": {
                    "id": technician_id,
                    "name": technician["name"],
                    "mobile": technician["mobile"]
                },
                "status": "Assigned"
            }}
        )

def close_ticket(ticket_id):
    ticket_collection.update_one(
        {"_id": ticket_id},
        {"$set": {"status": "Closed"}}
    )
