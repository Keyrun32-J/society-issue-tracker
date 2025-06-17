# app.py
import streamlit as st
from db import create_ticket, get_all_tickets, assign_ticket, close_ticket
from bson.objectid import ObjectId

st.set_page_config(page_title="Society Issue Tracker", layout="wide")

menu = st.sidebar.selectbox("Select View", ["Raise Ticket", "Manager Dashboard", "Technician View"])

if menu == "Raise Ticket":
    st.title("Raise a New Issue")
    flat = st.text_input("Flat Number (e.g. A-302)")
    issue_type = st.selectbox("Issue Type", ["Plumbing", "Electrical", "Tile", "Paint", "Door", "Other"])
    desc = st.text_area("Issue Description")
    raised_by = st.text_input("Your Name")
    if st.button("Submit Ticket"):
        if flat and desc and raised_by:
            create_ticket(flat, issue_type, desc, raised_by)
            st.success("✅ Ticket Raised Successfully!")
        else:
            st.error("❗ Please fill all the fields")

elif menu == "Manager Dashboard":
    st.title("Manager Dashboard")
    tickets = get_all_tickets()
    for t in tickets:
        st.markdown(f"### 📝 Ticket: {str(t['_id'])}")
        st.write(f"**Flat:** {t['flat_number']} | **Issue:** {t['issue_type']} | **Status:** {t['status']}")
        st.write(f"**Raised by:** {t['raised_by']}")
        st.write(f"**Description:** {t['description']}")
        if t['status'] == "Open":
            assignee = st.text_input(f"Assign to (Ticket ID: {str(t['_id'])})", key=f"assign_{str(t['_id'])}")
            if st.button(f"Assign", key=f"assign_btn_{str(t['_id'])}"):
                assign_ticket(str(t['_id']), assignee)
                st.success("🎯 Assigned successfully!")

elif menu == "Technician View":
    st.title("Technician Panel")
    name = st.text_input("Enter Your Name")
    if name:
        tickets = get_all_tickets()
        for t in tickets:
            if t.get("assigned_to") == name and t['status'] != "Closed":
                st.markdown(f"### 🔧 Ticket: {str(t['_id'])}")
                st.write(f"**Flat:** {t['flat_number']} | **Issue:** {t['issue_type']}")
                st.write(f"**Description:** {t['description']}")
                if st.button(f"Mark Closed (Ticket ID: {str(t['_id'])})", key=f"close_btn_{str(t['_id'])}"):
                    close_ticket(str(t['_id']))
                    st.success("✅ Ticket Closed!")
