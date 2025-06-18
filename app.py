import streamlit as st
from db import *
from bson.objectid import ObjectId
from datetime import datetime

st.set_page_config(page_title="Society Issue Tracker", layout="wide")

st.title("🏘️ Society Issue Tracker")

role = st.sidebar.selectbox("Login As", ["Resident", "Technician", "Manager"])

if role == "Resident":
    st.header("Raise a New Ticket")
    username = st.text_input("Your Name")
    flat = st.text_input("Flat Number")
    issue_type = st.selectbox("Issue Type", ["Electric", "Plumbing", "Carpentry", "Cleaning", "Others"])
    desc = st.text_area("Describe the Issue")
    priority = st.selectbox("Priority", ["P1 (6 Hrs)", "P2 (48 Hrs)", "P3 (5-10 Days)"])
    
    if st.button("Submit Ticket"):
        ticket = {
            'username': username,
            'flat': flat,
            'type': issue_type,
            'description': desc,
            'priority': priority.split()[0]  # P1, P2, P3
        }
        create_ticket(ticket)
        st.success("✅ Ticket Submitted Successfully!")

    st.subheader("📄 Your Tickets")
    if username:
        for ticket in get_user_tickets(username):
            st.markdown(f"**Type**: {ticket['type']} | **Priority**: {ticket['priority']} | **Status**: {ticket['status']}")
            if ticket.get('assigned_to'):
                st.markdown(f"**Assigned To**: {ticket['assigned_to']}")
            if ticket.get('due_date'):
                overdue = datetime.now() > ticket['due_date']
                due_status = "🚨 SLA Breached!" if overdue else "⏳ Within SLA"
                st.markdown(f"**SLA**: {ticket['due_date'].strftime('%Y-%m-%d %H:%M')} | {due_status}")
            st.markdown("---")

elif role == "Technician":
    st.header("Technician Login")
    uname = st.text_input("Username")
    pwd = st.text_input("Password", type="password")
    if st.button("Login"):
        tech = technician_login(uname, pwd)
        if tech:
            st.success(f"Welcome {tech['name']}!")
            st.subheader("🛠️ Assigned Tickets")
            for ticket in get_tickets_by_technician(tech['name']):
                st.markdown(f"**Flat**: {ticket['flat']} | **Type**: {ticket['type']} | **Status**: {ticket['status']}")
                if st.button(f"Mark Resolved: {ticket['_id']}", key=str(ticket['_id'])):
                    resolve_ticket(ticket['_id'])
                    st.experimental_rerun()
                st.markdown("---")
        else:
            st.error("Invalid Credentials")

elif role == "Manager":
    st.header("Manager Dashboard")

    tab1, tab2, tab3 = st.tabs(["📊 Overview", "🧑 Add Technicians", "📝 Assign Tickets"])

    with tab1:
        st.subheader("Tickets by Category")
        tickets = get_all_tickets()
        if tickets:
            buckets = {}
            for t in tickets:
                cat = t['type']
                stat = t['status']
                if cat not in buckets:
                    buckets[cat] = {'Open': 0, 'In Progress': 0, 'Resolved': 0}
                buckets[cat][stat] = buckets[cat].get(stat, 0) + 1
            
            for cat, stats in buckets.items():
                st.markdown(f"### {cat}")
                st.write(stats)

    with tab2:
        st.subheader("Add a New Technician")
        name = st.text_input("Technician Name")
        phone = st.text_input("Phone Number")
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")
        if st.button("Add Technician"):
            add_technician(name, phone, username, password)
            st.success("Technician Added")

    with tab3:
        st.subheader("Assign Tickets")
        for ticket in get_open_tickets():
            st.markdown(f"**Flat**: {ticket['flat']} | **Issue**: {ticket['type']} | **Desc**: {ticket['description']}")
            techs = get_technicians()
            tech_names = [t['name'] for t in techs]
            selected_tech = st.selectbox("Assign to Technician", tech_names, key=str(ticket['_id']))
            selected_priority = st.selectbox("Set Priority", ["P1", "P2", "P3"], key=f"pri_{ticket['_id']}")
            if st.button(f"Assign Ticket {ticket['_id']}", key=f"btn_{ticket['_id']}"):
                assign_ticket(ticket['_id'], selected_tech, selected_priority)
                st.success("Ticket Assigned")
                st.experimental_rerun()
