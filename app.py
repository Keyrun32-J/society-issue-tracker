import streamlit as st
from db import *
from datetime import datetime

st.set_page_config(page_title="Society Issue Tracker", layout="wide")

st.title("🏢 Society Issue Tracker")

view = st.sidebar.radio("Login As", ["Resident", "Manager", "Technician"])

# --- RESIDENT VIEW ---
if view == "Resident":
    st.subheader("Raise an Issue")
    flat = st.text_input("Flat Number")
    issue_type = st.selectbox("Issue Type", ["Electric", "Plumbing", "Carpentry", "Other"])
    description = st.text_area("Describe the issue")

    if st.button("Submit Ticket"):
        create_ticket({
            "flat": flat,
            "issue_type": issue_type,
            "description": description,
            "created_at": datetime.now(),
            "status": "Pending"
        })
        st.success("Ticket submitted!")

    st.subheader("Your Tickets")
    if flat:
        tickets = get_tickets_by_user(flat)
        for t in tickets:
            st.markdown(f"- **{t['issue_type']}** | {t['description']} | **Status:** {t.get('status', 'Pending')} | **Assigned To:** {t.get('assigned_to', 'N/A')} | Priority: {t.get('priority', '-')}")

# --- MANAGER VIEW ---
elif view == "Manager":
    st.subheader("Manager Dashboard")

    # Overview by Issue Type
    st.markdown("### 📊 Overview")
    all_tickets = get_all_tickets()
    issue_buckets = {}
    for t in all_tickets:
        typ = t.get("issue_type", "Unknown")
        issue_buckets.setdefault(typ, []).append(t)

    for category, items in issue_buckets.items():
        open_count = sum(1 for i in items if i.get("status") != "Resolved")
        closed_count = sum(1 for i in items if i.get("status") == "Resolved")
        st.markdown(f"**{category}** - Open: {open_count} | Closed: {closed_count}")

    # Assign Tickets
    st.markdown("### 🛠️ Assign Tickets")
    open_tickets = [t for t in all_tickets if t.get("status") != "Resolved"]

    if open_tickets:
        selected_ticket = st.selectbox("Select a ticket", open_tickets, format_func=lambda x: f"{x.get('_id')} - {x.get('issue_type', 'Unknown')}")
        technicians = get_technicians()
        tech_names = [t["name"] for t in technicians]

        selected_tech = st.selectbox("Assign to Technician", tech_names)
        selected_priority = st.radio("Priority", ["P1", "P2", "P3"])

        if st.button("Assign"):
            assign_ticket_to_technician(selected_ticket['_id'], selected_tech, selected_priority)
            st.success("Ticket assigned successfully!")
            st.experimental_rerun()
    else:
        st.info("No open tickets to assign.")

    # Add Technician
    st.markdown("### ➕ Add Technician")
    new_name = st.text_input("Technician Name")
    new_mobile = st.text_input("Mobile Number")
    if st.button("Add Technician"):
        add_technician(new_name, new_mobile)
        st.success("Technician added")

# --- TECHNICIAN VIEW ---
elif view == "Technician":
    st.subheader("Technician Login")
    tech_name = st.text_input("Enter your name")
    if tech_name:
        tickets = get_tickets_by_technician(tech_name)
        if tickets:
            st.subheader(f"Tickets assigned to {tech_name}")
            for t in tickets:
                breached = False
                if t.get("priority") == "P1":
                    due = t['created_at'] + timedelta(hours=6)
                elif t.get("priority") == "P2":
                    due = t['created_at'] + timedelta(hours=48)
                elif t.get("priority") == "P3":
                    due = t['created_at'] + timedelta(days=10)
                else:
                    due = t['created_at']

                if datetime.now() > due:
                    breached = True

                st.markdown(f"- **{t['issue_type']}** | {t['description']} | Priority: {t.get('priority')} | Status: {t.get('status')} | {'🚨 SLA Breached' if breached else '✅ On Time'}")
        else:
            st.info("No tickets assigned to you.")