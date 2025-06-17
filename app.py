# FILE: app.py
import streamlit as st
from db import create_ticket, get_all_tickets, assign_ticket, close_ticket, get_all_technicians
from bson import ObjectId

st.set_page_config(page_title="Society Issue Tracker", layout="wide")

st.title("🏡 Society Issue Tracker")

menu = st.sidebar.selectbox("Select View", ["Raise Ticket", "Manager Dashboard"])

if menu == "Raise Ticket":
    st.subheader("Raise a New Ticket")
    title = st.text_input("Title")
    description = st.text_area("Description")

    if st.button("Submit"):
        if title and description:
            create_ticket(title, description)
            st.success("Ticket submitted successfully!")
        else:
            st.warning("Please fill all fields.")

elif menu == "Manager Dashboard":
    st.subheader("📋 Manager Dashboard")

    tickets = get_all_tickets()
    technicians = get_all_technicians()
    technician_map = {tech['username']: tech['mobile'] for tech in technicians}

    for ticket in tickets:
        st.markdown(f"**Title**: {ticket['title']}")
        st.markdown(f"**Description**: {ticket['description']}")
        st.markdown(f"**Status**: {ticket['status']}")
        st.markdown(f"**Assigned To**: {ticket.get('assigned_to', 'Unassigned')}")
        st.markdown(f"**Mobile**: {ticket.get('mobile', '-')}")
        
        if ticket['status'] == "Open":
            tech_options = list(technician_map.keys())
            selected_tech = st.selectbox(f"Assign to Technician (Ticket ID: {ticket['_id']})", tech_options, key=str(ticket['_id']))
            if st.button("Assign", key=f"assign_{ticket['_id']}"):
                assign_ticket(ticket['_id'], selected_tech)
                st.success(f"Ticket assigned to {selected_tech}")
        
        if ticket['status'] != "Closed":
            if st.button("Close Ticket", key=f"close_{ticket['_id']}"):
                close_ticket(ticket['_id'])
                st.success("Ticket closed.")
        
        st.markdown("---")
