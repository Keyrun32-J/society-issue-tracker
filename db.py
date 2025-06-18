def assign_ticket_to_technician(ticket_id, technician_name, priority, status="In Progress"):
    ticket_collection.update_one(
        {"_id": ticket_id},
        {"$set": {"assigned_to": technician_name, "priority": priority, "status": status}}
    )
