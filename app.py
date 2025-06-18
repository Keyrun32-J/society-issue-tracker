# app.py
import streamlit as st
from datetime import datetime, timedelta
from db import (
    create_ticket, get_all_tickets, get_open_tickets, assign_ticket,
    get_technicians, get_tickets_by_resident, get_tickets_by_technician,
    update_ticket_status
)

# --- Hardcoded Credentials ---
MANAGER_CREDENTIALS = {"username": "manager", "password": "manager123"}
RESIDENT_CREDENTIALS = {"username": "resident", "password": "resident123"}
TECHNICIAN_PASSWORD = "tech123"

# --- Login Function ---
def login():
    st.title("🔐 Society Issue Tracker Login")
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")
    login_clicked = st.button("Login")

    if login_clicked:
        if username == MANAGER_CREDENTIALS["username"] and password == MANAGER_CREDENTIALS["password"]:
            st.session_state["role"] = "manager"
            st.session_state["username"] = username
        elif username == RESIDENT_CREDENTIALS["username"] and password == RESIDENT_CREDENTIALS["password"]:
            st.session_state["role"] = "resident"
            st.session_state["username"] = username
        else:
            technicians = get_technicians()
            for tech in technicians:
                if tech["username"] == username and password == TECHNICIAN_PASSWORD:
                    st.session_state["role"] = "technician"
                    st.session_state["username"] = username
                    break
            else:
                st.error("❌ Invalid credentials")

# --- Manager Dashboard ---
def manager_dashboard():
    st.header("🧱 Manager Dashboard")

    tickets = get_all_tickets()
    categories = {}
    for t in tickets:
        cat = t.get("issue_type", "Unknown")
        categories.setdefault(cat, []).append(t)

    for cat, ts in categories.items():
        st.subheader(f"{cat} Issues")
        st.write(f"Raised: {len(ts)}")
        st.write(f"Resolved: {sum(1 for t in ts if t.get('status') == 'Resolved')}")
        st.write(f"In Progress: {sum(1 for t in ts if t.get('status') == 'In Progress')}")

    # Assign Tickets
    st.subheader("Assign Ticket")
    open_tickets = get_open_tickets()
    if open_tickets:
        selected_ticket = st.selectbox("Select a ticket", open_tickets, format_func=lambda x: f"{x['_id']} - {x.get('issue_type', 'Unknown')}")
        technicians = get_technicians()
        selected_tech = st.selectbox("Assign Technician", [t["username"] for t in technicians])
        priority = st.selectbox("Set Priority", ["P1", "P2", "P3"])

        if st.button("Assign"):
            assign_ticket(selected_ticket["_id"], selected_tech, priority)
            st.success("Ticket assigned successfully!")
    else:
        st.info("No open tickets to assign.")

# --- Resident Dashboard ---
def resident_dashboard():
    st.header("🏠 Raise an Issue")

    flat_no = st.text_input("Flat Number")
    issue_type = st.selectbox("Issue Type", ["Electric", "Plumbing", "Carpentry", "Other"])
    description = st.text_area("Issue Description")

    if st.button("Submit"):
        create_ticket(flat_no, issue_type, description)
        st.success("Issue submitted!")

    st.subheader("🔍 Your Tickets")
    tickets = get_tickets_by_resident(st.session_state["username"])
    for t in tickets:
        st.write(f"**{t.get('issue_type')}** | {t.get('description')} | Status: {t.get('status', 'Pending')}")

# --- Technician Dashboard ---
def technician_dashboard():
    st.header(":man_mechanic: Technician Dashboard")
    username = st.session_state["username"]
    tickets = get_tickets_by_technician(username)
    now = datetime.now()

    for t in tickets:
        st.subheader(f"Ticket: {t.get('_id')}")
        st.write(f"Flat: {t.get('flat_no')}")
        st.write(f"Issue: {t.get('issue_type')} - {t.get('description')}")
        st.write(f"Priority: {t.get('priority')}")
        st.write(f"Status: {t.get('status', 'Pending')}")

        created_at = t.get("created_at")
        if created_at:
            created_at = datetime.strptime(created_at, "%Y-%m-%d %H:%M:%S")
            priority = t.get("priority", "P3")
            if priority == "P1":
                due = created_at + timedelta(hours=6)
            elif priority == "P2":
                due = created_at + timedelta(hours=48)
            else:
                due = created_at + timedelta(days=10)

            if now > due:
                st.error("SLA Breached!")
            else:
                st.success("Within SLA")

        if t.get("status") != "Resolved":
            if st.button(f"Mark Resolved - {t.get('_id')}"):
                update_ticket_status(t["_id"], "Resolved")
                st.success("Ticket marked as Resolved")
                st.experimental_rerun()

# --- App Logic ---
if "role" not in st.session_state:
    login()
    st.stop()

role = st.session_state["role"]

if role == "manager":
    manager_dashboard()
elif role == "resident":
    resident_dashboard()
elif role == "technician":
    technician_dashboard()
