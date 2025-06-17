# app.py
import streamlit as st
from bson import ObjectId
from db import create_ticket, get_all_tickets, assign_ticket, close_ticket, get_technicians, add_technician

st.set_page_config(page_title="Society Issue Tracker", layout="wide")
st.title("🏠 Society Issue Tracker")

menu = ["Resident", "Manager"]
choice = st.sidebar.selectbox("Who are you?", menu)

if choice == "Resident":
    st.header("Raise an Issue")
    flat_number = st.text_input("Flat Number")
    issue_type = st.selectbox("Issue Type", ["Electric", "Plumbing", "Carpentry", "Other"])
    description = st.text_area("Describe the issue")

    if st.button("Submit Ticket"):
        if flat_number and description:
            create_ticket(flat_number, issue_type, description)
            st.success("Ticket submitted successfully!")
        else:
            st.error("Please fill all fields")

elif choice == "Manager":
    st.header("Manager Dashboard")

    st.subheader("All Tickets")
    tickets = get_all_tickets()
    technicians = get_technicians()
    tech_dict = {tech["name"]: tech["mobile"] for tech in technicians}

    for ticket in tickets:
        with st.expander(f"Flat {ticket['flat_number']} - {ticket['issue_type']}"):
            st.markdown(f"**Description**: {ticket['description']}")
            st.markdown(f"**Status**: {ticket['status']}")
            assigned_to = ticket.get("assigned_to")
            if assigned_to:
                st.markdown(f"**Assigned To**: {assigned_to} ({tech_dict.get(assigned_to, 'No mobile')})")

            if ticket["status"] == "Open":
                tech_names = list(tech_dict.keys())
                selected_tech = st.selectbox("Assign to Technician", tech_names, key=str(ticket["_id"]))
                if st.button("Assign", key="assign_" + str(ticket["_id"])):
                    assign_ticket(ticket["_id"], selected_tech)
                    st.success("Assigned!")
                    st.experimental_rerun()

            if ticket["status"] != "Closed":
                if st.button("Close Ticket", key="close_" + str(ticket["_id"])):
                    close_ticket(ticket["_id"])
                    st.success("Ticket closed")
                    st.experimental_rerun()

    st.subheader("Technicians")
    for tech in technicians:
        st.markdown(f"- {tech['name']} 📞 {tech['mobile']}")

    st.subheader("Add New Technician")
    name = st.text_input("Technician Name")
    mobile = st.text_input("Mobile Number")

    if st.button("Add Technician"):
        if name and mobile:
            add_technician(name, mobile)
            st.success("Technician added")
            st.experimental_rerun()
        else:
            st.error("Enter both name and mobile")
