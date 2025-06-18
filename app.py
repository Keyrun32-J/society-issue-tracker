import streamlit as st
from db import (
    create_ticket, get_all_tickets, get_ticket_by_user, assign_ticket, close_ticket,
    get_all_technicians, get_tickets_by_technician, get_sla_breached_tickets,
    add_user, add_technician, get_user
)
from bson import ObjectId

# ----- Auth & Role Selection -----
role = st.sidebar.selectbox("Login As", ["Resident", "Manager", "Technician"])
username = st.sidebar.text_input("Username")

# For demo: show flat number/mobile entry only if resident
if role == "Resident" and st.sidebar.button("Register/Login"):
    flat_no = st.sidebar.text_input("Flat Number")
    mobile = st.sidebar.text_input("Mobile Number")
    add_user(username, flat_no, mobile)
    st.success("Logged in as Resident")

if role == "Technician" and st.sidebar.button("Register/Login"):
    name = st.sidebar.text_input("Name")
    mobile = st.sidebar.text_input("Mobile Number")
    add_technician(username, name, mobile)
    st.success("Logged in as Technician")

# ----- Resident Dashboard -----
if role == "Resident" and username:
    st.header("Raise New Issue")
    title = st.text_input("Issue Title")
    description = st.text_area("Description")
    issue_type = st.selectbox("Issue Type", ["Electric", "Plumbing", "Carpentry", "Other"])
    priority = st.selectbox("Priority", ["P1", "P2", "P3"])
    if st.button("Submit Ticket"):
        user = get_user(username)
        if user:
            create_ticket(user['flat_no'], title, description, issue_type, priority, username)
            st.success("Ticket submitted successfully")

    st.subheader("My Tickets")
    tickets = get_ticket_by_user(username)
    for t in tickets:
        st.markdown(f"**Title**: {t['title']}\n\n**Status**: {t['status']}\n\n**Assigned To**: {t.get('assigned_to', 'Not Assigned')}\n\n**Mobile**: {t.get('technician_mobile', 'N/A')}")
        st.markdown("---")

# ----- Manager Dashboard -----
if role == "Manager" and username:
    st.title("Manager Dashboard")

    all_tickets = get_all_tickets()
    buckets = {"Electric": [], "Plumbing": [], "Carpentry": [], "Other": []}
    for t in all_tickets:
        buckets[t['issue_type']].append(t)

    for category, tickets in buckets.items():
        st.subheader(f"{category} Issues")
        st.markdown(f"Total: {len(tickets)} | Resolved: {sum(1 for t in tickets if t['status']=='Resolved')} | In-Progress: {sum(1 for t in tickets if t['status']=='In Progress')} | Open: {sum(1 for t in tickets if t['status']=='Open')}")
        for t in tickets:
            st.markdown(f"**Title**: {t['title']}\n\n**Status**: {t['status']}\n\n**Priority**: {t['priority']}\n\n**Assigned To**: {t.get('assigned_to', 'Not Assigned')}\n\n**Flat**: {t['flat_no']}")
            if t['status'] == "Open":
                techs = get_all_technicians()
                selected = st.selectbox(f"Assign to Technician (Ticket: {t['_id']})", [tech['username'] for tech in techs], key=str(t['_id']))
                if st.button(f"Assign", key=f"assign_{t['_id']}"):
                    assign_ticket(t['_id'], selected)
                    st.success("Assigned successfully")
            if t['status'] != "Resolved" and st.button("Close Ticket", key=f"close_{t['_id']}"):
                close_ticket(t['_id'])
                st.success("Ticket Closed")
            st.markdown("---")

    st.subheader("SLA Breached Tickets")
    breached = get_sla_breached_tickets()
    for t in breached:
        st.error(f"⚠️ SLA Breached: {t['title']} (Flat {t['flat_no']})")

# ----- Technician Dashboard -----
if role == "Technician" and username:
    st.title("My Assigned Tickets")
    tickets = get_tickets_by_technician(username)
    breached = get_sla_breached_tickets(username)
    for t in tickets:
        st.markdown(f"**Title**: {t['title']}\n\n**Status**: {t['status']}\n\n**Priority**: {t['priority']}\n\n**Flat**: {t['flat_no']}")
        if t in breached:
            st.error("⚠️ SLA Breached")
        if t['status'] != "Resolved" and st.button("Mark as Resolved", key=str(t['_id'])):
            close_ticket(t['_id'])
            st.success("Resolved")
        st.markdown("---")
