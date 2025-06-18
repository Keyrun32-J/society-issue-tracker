import streamlit as st
from db import (
    create_ticket,
    get_all_tickets,
    get_tickets_by_user,
    assign_ticket_to_technician,
    add_technician,
    get_technicians,
    get_tickets_by_technician,
)
import datetime

st.set_page_config(page_title="Society Issue Tracker", layout="wide")
st.title("🏠 Society Issue Tracker")

role = st.sidebar.selectbox("Login as", ["Resident", "Manager", "Technician"])

# ------------------ RESIDENT ------------------ #
if role == "Resident":
    st.header("Raise an Issue")
    name = st.text_input("Your Name")
    flat = st.text_input("Flat Number")
    mobile = st.text_input("Mobile Number")
    issue_type = st.selectbox("Issue Type", ["Electrician", "Plumbing", "Carpentry", "Others"])
    description = st.text_area("Issue Description")

    if st.button("Submit"):
        ticket = {
            "name": name,
            "flat": flat,
            "mobile": mobile,
            "issue_type": issue_type,
            "description": description,
            "status": "Open",
            "priority": None,
            "assigned_to": None,
            "created_at": datetime.datetime.now()
        }
        create_ticket(ticket)
        st.success("✅ Ticket submitted!")

    st.markdown("---")
    st.subheader("Your Submitted Tickets")
    if flat:
        tickets = get_tickets_by_user(flat)
        for t in tickets:
            st.write(f"🔹 **Issue**: {t.get('issue_type', 'N/A')} | **Status**: {t.get('status', 'N/A')}")
            st.write(f"Description: {t.get('description', '')}")
            if t.get("assigned_to"):
                st.write(f"👨‍🔧 Assigned to: {t['assigned_to']}")

# ------------------ MANAGER ------------------ #
elif role == "Manager":
    st.header("Manager Dashboard")
    st.subheader("Overview by Category")
    tickets = get_all_tickets()
    category_status = {}

    for t in tickets:
        cat = t.get("issue_type", "Others")
        status = t.get("status", "Open")
        if cat not in category_status:
            category_status[cat] = {"Open": 0, "In Progress": 0, "Closed": 0}
        category_status[cat][status] = category_status[cat].get(status, 0) + 1

    for cat, status_count in category_status.items():
        st.write(f"🔧 **{cat}** — Open: {status_count['Open']}, In Progress: {status_count['In Progress']}, Closed: {status_count['Closed']}")

    st.markdown("---")
    st.subheader("Assign Ticket")
    open_tickets = [t for t in tickets if t.get("status") == "Open"]
    if open_tickets:
        selected_ticket = st.selectbox("Select a ticket", open_tickets, format_func=lambda x: f"{x.get('_id', '')} - {x.get('issue_type', '')}")
        technicians = get_technicians()
        selected_tech = st.selectbox("Assign to Technician", technicians, format_func=lambda x: f"{x['name']} ({x['mobile']})")
        priority = st.selectbox("Set Priority", ["P1", "P2", "P3"])  # SLA related

        if st.button("Assign"):
            assign_ticket_to_technician(selected_ticket["_id"], selected_tech["name"], priority)
            st.success("✅ Ticket Assigned")
            st.experimental_rerun()
    else:
        st.info("No open tickets to assign.")

    st.markdown("---")
    st.subheader("Assigned Tickets")
    assigned_tickets = [t for t in tickets if t.get("assigned_to")]
    for t in assigned_tickets:
        st.write(f"📌 **Issue**: {t.get('issue_type', '')}")
        st.write(f"👤 Resident: {t.get('name')} | 🏠 Flat: {t.get('flat')}")
        st.write(f"📞 Mobile: {t.get('mobile')}")
        st.write(f"🛠️ Assigned to: {t.get('assigned_to')} | 🚦 Priority: {t.get('priority', 'Not Set')} | 📌 Status: {t.get('status', '')}")
        st.markdown("---")

    st.subheader("Add Technician")
    new_tech_name = st.text_input("Technician Name")
    new_tech_mobile = st.text_input("Technician Mobile Number")
    if st.button("Add Technician"):
        add_technician(new_tech_name, new_tech_mobile)
        st.success("✅ Technician Added")

# ------------------ TECHNICIAN ------------------ #
elif role == "Technician":
    st.header("Technician Dashboard")
    tech_name = st.text_input("Enter your name")
    if tech_name:
        tickets = get_tickets_by_technician(tech_name)
        if tickets:
            for t in tickets:
                st.write(f"🔧 **Issue**: {t.get('issue_type', '')}")
                st.write(f"📄 Description: {t.get('description', '')}")
                st.write(f"🏠 Flat: {t.get('flat', '')}")
                st.write(f"📌 Priority: {t.get('priority', '')}")
                st.write(f"📍 Status: {t.get('status', '')}")
                if st.button(f"Mark as In Progress - {t['_id']}"):
                    assign_ticket_to_technician(t["_id"], tech_name, t.get("priority"), status="In Progress")
                    st.experimental_rerun()
                if st.button(f"Mark as Closed - {t['_id']}"):
                    assign_ticket_to_technician(t["_id"], tech_name, t.get("priority"), status="Closed")
                    st.experimental_rerun()
                st.markdown("---")
        else:
            st.info("No tickets assigned to you.")
