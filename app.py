import streamlit as st
from config import ticket_collection, technicians
from pymongo import ASCENDING

# ---------- Helper Functions ----------

def create_ticket(title, description, mobile):
    ticket = {
        "title": title,
        "description": description,
        "mobile": mobile,
        "status": "Open",
        "assigned_to": None
    }
    ticket_collection.insert_one(ticket)

def get_all_tickets():
    return list(ticket_collection.find().sort("_id", ASCENDING))

def assign_ticket(ticket_id, technician_key):
    technician = technicians[technician_key]
    ticket_collection.update_one(
        {"_id": ticket_id},
        {"$set": {"assigned_to": technician_key}}
    )

def close_ticket(ticket_id):
    ticket_collection.update_one(
        {"_id": ticket_id},
        {"$set": {"status": "Closed"}}
    )

# ---------- Streamlit App ----------

st.title("🏢 Society Issue Tracker")

menu = st.sidebar.radio("Navigation", ["Resident", "Manager"])

# ---------- Resident View ----------
if menu == "Resident":
    st.header("Report an Issue")

    with st.form("ticket_form"):
        title = st.text_input("Issue Title")
        description = st.text_area("Issue Description")
        mobile = st.text_input("Your Mobile Number")

        submitted = st.form_submit_button("Submit")
        if submitted:
            if title and description and mobile:
                create_ticket(title, description, mobile)
                st.success("✅ Ticket created successfully!")
            else:
                st.warning("Please fill all the fields.")

# ---------- Manager View ----------
elif menu == "Manager":
    st.header("📋 Manager Dashboard")
    tickets = get_all_tickets()

    if not tickets:
        st.info("No tickets submitted yet.")
    else:
        for ticket in tickets:
            with st.expander(f"📝 {ticket['title']} - [{ticket['status']}]"):
                st.markdown(f"**Description**: {ticket['description']}")
                st.markdown(f"**Mobile**: {ticket.get('mobile', 'N/A')}")
                assigned_key = ticket.get("assigned_to")
                if assigned_key:
                    assigned_info = technicians.get(assigned_key, {})
                    st.markdown(f"**Assigned To**: {assigned_info.get('name')} ({assigned_info.get('mobile')})")
                else:
                    st.markdown("**Assigned To**: Not yet assigned")

                # Assignment options
                if ticket["status"] != "Closed":
                    cols = st.columns(2)

                    with cols[0]:
                        selected_tech = st.selectbox(
                            "Assign Technician",
                            options=list(technicians.keys()),
                            format_func=lambda k: f"{technicians[k]['name']} ({technicians[k]['mobile']})",
                            key=f"tech_{str(ticket['_id'])}"
                        )

                        if st.button("Assign", key=f"assign_{str(ticket['_id'])}"):
                            assign_ticket(ticket["_id"], selected_tech)
                            st.success("✅ Ticket assigned.")
                            st.experimental_rerun()

                    with cols[1]:
                        if st.button("Close Ticket", key=f"close_{str(ticket['_id'])}"):
                            close_ticket(ticket["_id"])
                            st.success("✅ Ticket closed.")
                            st.experimental_rerun()
