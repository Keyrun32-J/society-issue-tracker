# app.py
import streamlit as st
from db import (
    create_ticket, get_all_tickets, assign_ticket,
    get_tickets_by_user, get_technicians, update_ticket_status, create_user,
    authenticate_user, create_technician, get_tickets_by_technician
)

st.set_page_config(page_title="Society Issue Tracker", layout="wide")
st.title("🏢 Society Issue Tracker")

menu = ["Resident", "Manager", "Technician"]
choice = st.sidebar.selectbox("Login as", menu)

if choice == "Resident":
    st.subheader("Raise an Issue")
    username = st.text_input("Enter your flat number or name")
    password = st.text_input("Password", type="password")
    if st.button("Login/Register"):
        create_user(username, password)
        st.session_state["user"] = username

    if "user" in st.session_state:
        issue_type = st.selectbox("Issue Type", ["Electric", "Plumbing", "Carpentry", "Other"])
        description = st.text_area("Describe the issue")
        if st.button("Submit Ticket"):
            create_ticket(st.session_state["user"], issue_type, description)
            st.success("Ticket submitted successfully!")

        st.subheader("Your Tickets")
        tickets = get_tickets_by_user(st.session_state["user"])
        for ticket in tickets:
            st.markdown(f"**Issue**: {ticket['issue_type']}")
            st.markdown(f"**Description**: {ticket['description']}")
            st.markdown(f"**Status**: {ticket['status']}")
            st.markdown(f"**Technician**: {ticket.get('technician', 'Not assigned')}")
            st.markdown(f"**Priority**: {ticket.get('priority', 'Not set')}")
            st.markdown("---")

elif choice == "Manager":
    st.subheader("Manager Dashboard")

    # Ticket overview by issue type and status
    tickets = get_all_tickets()
    st.subheader("📊 Ticket Overview")
    stats = {}
    for t in tickets:
        issue_type = t.get("issue_type", "Uncategorized")
        status = t.get("status", "Unknown")
        if issue_type not in stats:
            stats[issue_type] = {"Open": 0, "In Progress": 0, "Closed": 0}
        if status not in stats[issue_type]:
            stats[issue_type][status] = 0
        stats[issue_type][status] += 1

    for category, stat in stats.items():
        st.markdown(f"**🛠️ {category}**")
        col1, col2, col3 = st.columns(3)
        col1.metric("Open", stat.get("Open", 0))
        col2.metric("In Progress", stat.get("In Progress", 0))
        col3.metric("Closed", stat.get("Closed", 0))
        st.divider()

    st.subheader("Assign Tickets")
    open_tickets = [t for t in tickets if t.get("status") == "Open"]
    if open_tickets:
        selected_ticket = st.selectbox("Select a ticket", open_tickets, format_func=lambda x: f"{x['_id']} - {x.get('issue_type', 'Unknown')}")
        technicians = get_technicians()
        tech_map = {f"{tech['name']} ({tech['mobile']})": tech["username"] for tech in technicians}
        selected_tech = st.selectbox("Assign to Technician", list(tech_map.keys()))
        priority = st.selectbox("Select Priority", ["P1", "P2", "P3"])
        if st.button("Assign"):
            assign_ticket(selected_ticket["_id"], tech_map[selected_tech], priority)
            st.success("Ticket assigned successfully!")
            st.experimental_rerun()
    else:
        st.info("No open tickets to assign.")

    st.subheader("Technician Management")
    new_tech_name = st.text_input("Technician Name")
    new_tech_mobile = st.text_input("Mobile Number")
    new_tech_username = st.text_input("Username")
    new_tech_password = st.text_input("Password", type="password")
    if st.button("Add Technician"):
        create_technician(new_tech_name, new_tech_mobile, new_tech_username, new_tech_password)
        st.success("Technician added successfully")

elif choice == "Technician":
    st.subheader("Technician Login")
    tech_username = st.text_input("Username")
    tech_password = st.text_input("Password", type="password")
    if st.button("Login"):
        if authenticate_user(tech_username, tech_password, user_type="technician"):
            st.session_state["technician"] = tech_username
        else:
            st.error("Invalid credentials")

    if "technician" in st.session_state:
        st.success(f"Welcome, {st.session_state['technician']}")
        my_tickets = get_tickets_by_technician(st.session_state["technician"])
        st.subheader("My Tickets")
        for ticket in my_tickets:
            st.markdown(f"**Issue**: {ticket['issue_type']}")
            st.markdown(f"**Description**: {ticket['description']}")
            st.markdown(f"**Priority**: {ticket.get('priority', 'Not set')}")
            st.markdown(f"**Status**: {ticket['status']}")
            if ticket['status'] != "Closed":
                if st.button(f"Mark as In Progress - {ticket['_id']}"):
                    update_ticket_status(ticket['_id'], "In Progress")
                    st.experimental_rerun()
                if st.button(f"Close Ticket - {ticket['_id']}"):
                    update_ticket_status(ticket['_id'], "Closed")
                    st.experimental_rerun()
            st.markdown("---")
