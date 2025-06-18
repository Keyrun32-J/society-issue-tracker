import streamlit as st
from db import (
    create_ticket, get_all_tickets, get_open_tickets, assign_ticket,
    close_ticket, get_tickets_by_flat, get_tickets_by_technician,
    get_technicians, add_technician
)
from datetime import datetime, timedelta

# Hardcoded credentials
USERS = {
    "resident1": {"role": "resident", "flat": "A-101"},
    "manager": {"role": "manager"},
    "tech1": {"role": "technician"},
    "tech2": {"role": "technician"},
}

st.set_page_config(page_title="Society Issue Tracker", layout="wide")
st.title("🏢 Society Issue Tracker")

username = st.text_input("Username")
password = st.text_input("Password", type="password")

if st.button("Login"):
    if username in USERS:
        role = USERS[username]["role"]
        st.session_state["role"] = role
        st.session_state["username"] = username
        st.success(f"Logged in as {role.capitalize()}")
    else:
        st.error("Invalid credentials")

if "role" not in st.session_state:
    st.stop()

role = st.session_state["role"]
username = st.session_state["username"]

if role == "resident":
    st.header(f"Resident Dashboard - {USERS[username]['flat']}")
    
    st.subheader("Raise an Issue")
    issue_type = st.selectbox("Issue Type", ["Electric", "Plumbing", "Carpentry"])
    description = st.text_area("Describe the issue")
    priority = st.selectbox("Priority", ["P1", "P2", "P3"])
    
    if st.button("Submit Ticket"):
        create_ticket(USERS[username]['flat'], issue_type, description, priority)
        st.success("Ticket submitted successfully!")

    st.subheader("Your Tickets")
    tickets = get_tickets_by_flat(USERS[username]['flat'])
    for t in tickets:
        st.markdown(f"""
        **Ticket ID**: {str(t["_id"])}  
        **Issue**: {t['issue_type']}  
        **Description**: {t['description']}  
        **Priority**: {t['priority']}  
        **Status**: {t['status']}  
        **Assigned To**: {t.get('assigned_to', 'Not Assigned')}  
        """)

elif role == "manager":
    st.header("Manager Dashboard")

    st.subheader("Add Technician")
    new_username = st.text_input("Technician Username")
    mobile = st.text_input("Mobile Number")
    if st.button("Add Technician"):
        add_technician(new_username, mobile)
        st.success("Technician added.")

    st.subheader("Assign Tickets")
    open_tickets = get_open_tickets()
    if open_tickets:
        selected_ticket = st.selectbox("Select Ticket", open_tickets, format_func=lambda x: f"{x['_id']} - {x['issue_type']} ({x['priority']})")
        available_techs = get_technicians()
        selected_tech = st.selectbox("Assign to", available_techs, format_func=lambda x: f"{x['username']} ({x['mobile']})")
        if st.button("Assign"):
            assign_ticket(selected_ticket["_id"], selected_tech["username"])
            st.success("Ticket assigned.")
    else:
        st.info("No open tickets.")

    st.subheader("Overview")
    all_tickets = get_all_tickets()
    summary = {}
    for t in all_tickets:
        cat = t["issue_type"]
        summary.setdefault(cat, {"Open": 0, "In Progress": 0, "Resolved": 0})
        summary[cat][t["status"]] += 1

    for issue_type, data in summary.items():
        st.markdown(f"### {issue_type}")
        st.write(data)

elif role == "technician":
    st.header(f"Technician Dashboard - {username}")
    tickets = get_tickets_by_technician(username)
    now = datetime.utcnow()

    for t in tickets:
        st.markdown(f"#### Ticket ID: {t['_id']}")
        st.write(f"**Flat**: {t['flat']}")
        st.write(f"**Issue**: {t['issue_type']}")
        st.write(f"**Description**: {t['description']}")
        st.write(f"**Priority**: {t['priority']}")
        st.write(f"**Status**: {t.get('status', 'Pending')}")

        created = t.get("assigned_at", t.get("created_at"))
        sla_hours = {"P1": 6, "P2": 48, "P3": 120}
        due = created + timedelta(hours=sla_hours.get(t['priority'], 48))
        
        if now > due:
            st.warning("⚠️ SLA Breached")
        else:
            st.success(f"Within SLA. Due by: {due.strftime('%Y-%m-%d %H:%M')}")

        if t["status"] != "Resolved":
            if st.button(f"Mark Resolved - {t['_id']}", key=str(t["_id"])):
                close_ticket(t["_id"])
                st.success("Ticket marked as resolved.")
