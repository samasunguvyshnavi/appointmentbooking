import streamlit as st
from datetime import datetime, timedelta
import pandas as pd

# Set up app
st.set_page_config(page_title="📅 Appointment Booking Bot", layout="centered")
st.title("📅 Appointment Booking Chatbot")

# Initialize session state
if "bookings" not in st.session_state:
    st.session_state.bookings = []

# Step-by-step inputs
with st.form("booking_form"):
    st.subheader("👤 Your Information")
    name = st.text_input("Enter your full name")
    email = st.text_input("Email (optional)")
    
    st.subheader("🛎️ Choose Service")
    service = st.selectbox("Select a service", ["Doctor", "Salon", "Consultant"])
    
    st.subheader("📅 Select Date and Time")
    date = st.date_input("Appointment Date", min_value=datetime.now().date())
    time = st.time_input("Appointment Time", value=(datetime.now() + timedelta(hours=1)).time())
    
    submitted = st.form_submit_button("Book Appointment")

# Confirm booking
if submitted:
    appointment_dt = datetime.combine(date, time)
    if appointment_dt < datetime.now():
        st.error("⛔ Please select a future time.")
    else:
        # Check if slot already booked
        slot_taken = any(
            b["datetime"] == appointment_dt and b["service"] == service
            for b in st.session_state.bookings
        )
        if slot_taken:
            st.warning("⚠️ This time slot is already booked for the selected service. Please pick another time.")
        else:
            booking = {
                "name": name,
                "email": email,
                "service": service,
                "datetime": appointment_dt
            }
            st.session_state.bookings.append(booking)

            st.success("✅ Appointment Confirmed!")
            st.info(f"""
**👤 Name:** {name}  
**🛎️ Service:** {service}  
**📅 Date & Time:** {appointment_dt.strftime("%A, %d %B %Y at %I:%M %p")}  
{"**📧 Email:** " + email if email else ""}
            """)

# Display current bookings
if st.session_state.bookings:
    st.write("---")
    st.subheader("📋 All Bookings")
    df = pd.DataFrame(st.session_state.bookings)
    df["datetime"] = df["datetime"].dt.strftime("%Y-%m-%d %I:%M %p")
    st.dataframe(df, use_container_width=True)

    # Download CSV
    csv = df.to_csv(index=False).encode('utf-8')
    st.download_button("⬇️ Download Bookings CSV", data=csv, file_name="appointments.csv", mime="text/csv")

# Clear all
if st.button("🧹 Clear All Bookings"):
    st.session_state.bookings = []
    st.success("All bookings cleared.")
