import streamlit as st
from db import (
    create_ticket, get_tickets_by_flat, get_all_tickets,
    assign_ticket, get_open_tickets, get_technician_tickets,
    close_ticket, get_all_technicians, get_technician_details,
    authenticate_user
)
from datetime import datetime, timedelta

# Hardcoded user roles
st.sidebar.title("Login")
role = st.sidebar.selectbox("Role", ["resident", "manager", "technician"])
username = st.sidebar.text_input("Username")
login = st.sidebar.button("Login")

if login:
    if authenticate_user(username, role):
        st.success(f"Logged in as {username} ({role})")

        if role == "resident":
            st.header("Raise a Ticket")
            flat_no = st.text_input("Flat Number")
            issue_type = st.selectbox("Issue Type", ["Electric", "Plumbing", "Carpentry", "Others"])
            description = st.text_area("Issue Description")
            if st.button("Submit Ticket"):
                create_ticket(flat_no, issue_type, description)
                st.success("Ticket submitted successfully")

            st.header("My Tickets")
            if flat_no:
                tickets = get_tickets_by_flat(flat_no)
                for t in tickets:
                    st.markdown(f"**Type**: {t['issue_type']}")
                    st.markdown(f"**Description**: {t['description']}")
                    st.markdown(f"**Status**: {t.get('status', 'Unknown')}")
                    st.markdown(f"**Assigned To**: {t.get('assigned_to', 'Unassigned')}")
                    st.markdown(f"**Priority**: {t.get('priority', 'None')}")
                    st.divider()

        elif role == "manager":
            st.header("Manager Dashboard")
            tickets = get_all_tickets()
            open_tickets = get_open_tickets()
            stats = {}
            for t in tickets:
                cat = t.get("issue_type", "Unknown")
                if cat not in stats:
                    stats[cat] = {"Open": 0, "In Progress": 0, "Closed": 0}
                stats[cat][t.get("status", "Open")] += 1

            st.subheader("Ticket Overview")
            for k, v in stats.items():
                st.write(f"**{k}** - Open: {v['Open']}, In Progress: {v['In Progress']}, Closed: {v['Closed']}")

            st.subheader("Assign Tickets")
            if open_tickets:
                selected_ticket = st.selectbox(
                    "Select a ticket",
                    open_tickets,
                    format_func=lambda x: f"{x['_id']} - {x.get('issue_type', 'Unknown')}"
                )
                technicians = get_all_technicians()
                tech_names = [t['username'] for t in technicians]
                selected_tech = st.selectbox("Assign Technician", tech_names)
                priority = st.selectbox("Priority", ["P1", "P2", "P3"])
                if st.button("Assign"):
                    assign_ticket(selected_ticket['_id'], selected_tech, priority)
                    st.success("Ticket assigned")
                    st.experimental_rerun()
            else:
                st.info("No open tickets")

        elif role == "technician":
            st.header("Technician Dashboard")
            tickets = get_technician_tickets(username)
            if tickets:
                for t in tickets:
                    st.markdown(f"**Flat**: {t['flat_no']}")
                    st.markdown(f"**Issue**: {t['issue_type']}")
                    st.markdown(f"**Description**: {t['description']}")
                    st.markdown(f"**Status**: {t.get('status', 'Pending')}")
                    st.markdown(f"**Priority**: {t.get('priority', 'None')}")
                    if t.get("created_at"):
                        due = None
                        if t['priority'] == "P1":
                            due = t['created_at'] + timedelta(hours=6)
                        elif t['priority'] == "P2":
                            due = t['created_at'] + timedelta(hours=48)
                        elif t['priority'] == "P3":
                            due = t['created_at'] + timedelta(days=10)
                        if due:
                            now = datetime.utcnow()
                            status = "✅ On Time" if now <= due else "❌ SLA Breached"
                            st.markdown(f"**SLA Due**: {due.strftime('%Y-%m-%d %H:%M:%S')} ({status})")
                    if t.get("status") != "Closed" and st.button("Mark Closed", key=str(t["_id"])):
                        close_ticket(t['_id'])
                        st.success("Ticket Closed")
                        st.experimental_rerun()
                    st.divider()
            else:
                st.info("No tickets assigned")

    else:
        st.error("Authentication failed. Please check your username and role.")
