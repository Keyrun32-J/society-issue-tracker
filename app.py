import streamlit as st
from db import (
    create_ticket,
    get_all_tickets,
    get_tickets_by_user,
    assign_ticket,
    get_technicians,
    get_technician_tickets,
    update_ticket_status,
)
from datetime import datetime
import uuid

st.set_page_config(page_title="Society Issue Tracker", layout="wide")
st.title("🏢 Society Issue Tracker")

# --- Role Selection ---
role = st.sidebar.radio("Login as:", ["Resident", "Manager", "Technician"])

# --- Resident View ---
if role == "Resident":
    st.header("Raise an Issue")
    name = st.text_input("Your Name")
    flat = st.text_input("Flat Number")
    issue_type = st.selectbox("Issue Type", ["Electric", "Plumbing", "Carpentry", "Other"])
    description = st.text_area("Issue Description")

    if st.button("Submit Ticket"):
        if name and flat and description:
            create_ticket(name, flat, issue_type, description)
            st.success("Ticket submitted successfully!")
        else:
            st.warning("Please fill in all fields")

    st.divider()
    st.subheader("Your Raised Tickets")
    if name and flat:
        user_tickets = get_tickets_by_user(name, flat)
        if user_tickets:
            for t in user_tickets:
                st.markdown(f"**Ticket ID**: {t['_id']}")
                st.markdown(f"**Issue**: {t['issue_type']} | **Description**: {t['description']}")
                st.markdown(f"**Status**: {t['status']} | **Priority**: {t.get('priority', 'Not set')}")
                assigned = t.get("assigned_to")
                if assigned:
                    st.markdown(f"**Assigned Technician**: {assigned.get('name')} | 📞 {assigned.get('mobile')}")
                st.markdown("---")
        else:
            st.info("No tickets found for your flat.")

# --- Manager View ---
elif role == "Manager":
    st.header("Manager Dashboard")
    tickets = get_all_tickets()
    techs = get_technicians()

    # Grouped stats
    category_summary = {}
    for t in tickets:
        cat = t["issue_type"]
        category_summary.setdefault(cat, {"Total": 0, "In Progress": 0, "Resolved": 0})
        category_summary[cat]["Total"] += 1
        category_summary[cat][t["status"]] += 1

    st.subheader("📊 Category-wise Ticket Status")
    for cat, stat in category_summary.items():
        st.markdown(f"**{cat}** — Total: {stat['Total']} | In Progress: {stat['In Progress']} | Resolved: {stat['Resolved']}")

    st.divider()
    st.subheader("🛠 Assign Tickets")

    unassigned_tickets = [t for t in tickets if t["status"] == "Open"]
    for t in unassigned_tickets:
        st.markdown(f"**Ticket ID**: {t['_id']} | **Flat**: {t['flat']} | {t['issue_type']}")
        st.markdown(f"**Description**: {t['description']}")

        tech_names = [tech["name"] for tech in techs]
        selected_tech_name = st.selectbox("Select Technician", tech_names, key=f"tech_{t['_id']}")
        priority = st.selectbox("Select Priority", ["P1", "P2", "P3"], key=f"prio_{t['_id']}")

        selected_tech = next((tech for tech in techs if tech["name"] == selected_tech_name), None)

        if st.button("Assign", key=f"assign_{t['_id']}"):
            assign_ticket(t["_id"], selected_tech["_id"], priority)
            st.success(f"Ticket assigned to {selected_tech['name']} with {priority}")
            st.rerun()

    st.divider()
    st.subheader("Add New Technician")
    tech_name = st.text_input("Technician Name")
    mobile = st.text_input("Mobile Number")
    tech_username = st.text_input("Username")
    tech_password = st.text_input("Password", type="password")

    if st.button("Add Technician"):
        from db import add_technician
        add_technician(tech_name, mobile, tech_username, tech_password)
        st.success("Technician added successfully")
        st.rerun()

# --- Technician View ---
elif role == "Technician":
    st.header("Technician Login")
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    if st.button("Login"):
        from db import authenticate_technician
        tech = authenticate_technician(username, password)
        if tech:
            st.success(f"Welcome {tech['name']}")
            st.subheader("Your Assigned Tickets")

            tickets = get_technician_tickets(tech["_id"])
            for t in tickets:
                st.markdown(f"**Ticket ID**: {t['_id']} | Flat: {t['flat']} | {t['issue_type']}")
                st.markdown(f"**Priority**: {t.get('priority')} | **Status**: {t['status']}")
                st.markdown(f"**Description**: {t['description']}")

                new_status = st.selectbox("Update Status", ["In Progress", "Resolved"], key=f"status_{t['_id']}")
                if st.button("Update Status", key=f"update_{t['_id']}"):
                    update_ticket_status(t["_id"], new_status)
                    st.success("Status updated")
                    st.rerun()
                st.markdown("---")
        else:
            st.error("Invalid login credentials")
