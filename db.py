from config import ticket_collection, technician_collection, user_collection
from datetime import datetime, timedelta

def create_ticket(ticket):
    ticket['created_at'] = datetime.now()
    ticket['status'] = 'Open'
    ticket['assigned_to'] = None
    ticket_collection.insert_one(ticket)

def get_user_tickets(username):
    return list(ticket_collection.find({'username': username}))

def get_all_tickets():
    return list(ticket_collection.find())

def get_open_tickets():
    return list(ticket_collection.find({'status': 'Open'}))

def assign_ticket(ticket_id, technician_name, priority):
    priority_sla = {
        'P1': 6,
        'P2': 48,
        'P3': 120  # ~5 business days
    }
    sla_hours = priority_sla.get(priority, 48)
    due_date = datetime.now() + timedelta(hours=sla_hours)

    ticket_collection.update_one(
        {'_id': ticket_id},
        {'$set': {
            'assigned_to': technician_name,
            'priority': priority,
            'status': 'In Progress',
            'due_date': due_date
        }}
    )

def resolve_ticket(ticket_id):
    ticket_collection.update_one(
        {'_id': ticket_id},
        {'$set': {'status': 'Resolved', 'resolved_at': datetime.now()}}
    )

def add_technician(name, phone, username, password):
    technician_collection.insert_one({
        'name': name,
        'phone': phone,
        'username': username,
        'password': password
    })

def get_technicians():
    return list(technician_collection.find())

def technician_login(username, password):
    return technician_collection.find_one({'username': username, 'password': password})

def get_tickets_by_technician(tech_name):
    return list(ticket_collection.find({'assigned_to': tech_name}))
