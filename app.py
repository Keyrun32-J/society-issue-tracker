import streamlit as st
from db import (
    create_ticket,
    get_all_tickets,
    assign_ticket,
    get_tickets_by_user,
    create_user,
    validate_user,
    get_all_technicians,
    create_technician,
    get_tickets_by_technician,
    get_open_tickets
)

st.set_page_config(page_title="Society Issue Tracker")
st.title("🏡 Society Issue Tracker")

# Login Section
role = st.sidebar.selectbox("Select Role", ["Resident", "Manager", "Technician"])
username = st.sidebar.text_input("Username")
password = st.sidebar.text_input("Password", type="password")

if st.sidebar.button("Login"):
    user = validate_user(username, password, role)
    if not user:
        st.sidebar.error("Invalid credentials or user not found.")
    else:
        st.session_state.logged_in = True
        st.session_state.role = role
        st.session_state.username = username
        st.experimental_rerun()

# Sign Up Section (only for residents for now)
if st.sidebar.checkbox("New Resident? Register Here"):
    new_user = st.sidebar.text_input("New Username")
    new_pass = st.sidebar.text_input("New Password", type="password")
    flat = st.sidebar.text_input("Flat Number")
    if st.sidebar.button("Register"):
        create_user(new_user, new_pass, flat)
        st.sidebar.success("User registered! Please login.")

# If logged in
if st.session_state.get("logged_in"):
    st.success(f"Logged in as {st.session_state.username} ({st.session_state.role})")

    if st.session_state.role == "Resident":
        st.header("Raise an Issue")
        issue_type = st.selectbox("Issue Type", ["Electrician", "Plumber", "Carpenter", "Other"])
        description = st.text_area("Issue Description")
        priority = st.selectbox("Priority", ["P1", "P2", "P3"])

        if st.button("Submit Ticket"):
            create_ticket(
                raised_by=st.session_state.username,
                issue_type=issue_type,
                description=description,
                priority=priority
            )
            st.success("Ticket Submitted")

        st.header("Your Tickets")
        tickets = get_tickets_by_user(st.session_state.username)
        for t in tickets:
            st.write(f"**ID**: {t['_id']}")
            st.write(f"**Issue**: {t.get('issue_type', 'Unknown')}")
            st.write(f"**Description**: {t.get('description', '')}")
            st.write(f"**Status**: {t.get('status', 'Pending')}")
            st.write(f"**Assigned Technician**: {t.get('assigned_to', 'Not Assigned')}")
            st.markdown("---")

    elif st.session_state.role == "Manager":
        st.header("Manager Dashboard")

        st.subheader("Overview")
        all_tickets = get_all_tickets()
        counts = {"Electrician": 0, "Plumber": 0, "Carpenter": 0, "Other": 0}
        for t in all_tickets:
            cat = t.get("issue_type", "Other")
            if cat in counts:
                counts[cat] += 1
        for cat, count in counts.items():
            st.write(f"{cat}: {count} tickets")

        st.subheader("Assign Ticket")
        open_tickets = get_open_tickets()
        open_tickets = [t for t in open_tickets if isinstance(t, dict) and '_id' in t]

        if open_tickets:
            selected_ticket = st.selectbox(
                "Select a ticket",
                open_tickets,
                format_func=lambda x: f"{x.get('_id', '')} - {x.get('issue_type', 'Unknown')}"
            )
            technicians = get_all_technicians()
            selected_tech = st.selectbox("Assign to Technician", [tech['name'] for tech in technicians])
            selected_priority = st.selectbox("Priority", ["P1", "P2", "P3"])

            if st.button("Assign"):
                assign_ticket(selected_ticket['_id'], selected_tech, selected_priority)
                st.success("Ticket Assigned")
                st.experimental_rerun()
        else:
            st.info("No open tickets available.")

        st.subheader("Add Technician")
        tech_name = st.text_input("Technician Name")
        tech_mobile = st.text_input("Mobile Number")
        if st.button("Add Technician"):
            create_technician(tech_name, tech_mobile)
            st.success("Technician added")

    elif st.session_state.role == "Technician":
        st.header("Technician Dashboard")
        tickets = get_tickets_by_technician(st.session_state.username)
        for t in tickets:
            st.write(f"**ID**: {t['_id']}")
            st.write(f"**Issue**: {t.get('issue_type', 'Unknown')}")
            st.write(f"**Description**: {t.get('description', '')}")
            st.write(f"**Priority**: {t.get('priority', '')}")
            st.write(f"**Status**: {t.get('status', 'Pending')}")
            st.markdown("---")
