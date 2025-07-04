import streamlit as st
import pandas as pd
from datetime import datetime
from src.agent import WaterIntakeAgent
from src.water_intake_database import get_intake_history, log_intake

# Initialize session state
if "tracker_started" not in st.session_state:
    st.session_state.tracker_started = False

st.title("Water Intake Tracker")

if not st.session_state.tracker_started:
    st.write("Welcome to the Water Intake Tracker!")
    st.write("Please enter your details to start tracking your water intake.")

    if st.button("Start Tracking"):
        st.session_state.tracker_started = True
        st.rerun()  # Properly refresh after session state update
else:
    st.sidebar.header("User Details")
    user_id = st.sidebar.text_input("User ID")

    st.sidebar.write("---")
    st.sidebar.header("Water Intake")
    intake_ml = st.sidebar.number_input("Enter intake (ml)", min_value=0)

    if st.sidebar.button("Log Intake"):
        if user_id:
            log_intake(user_id, intake_ml)
            st.sidebar.success("Intake logged successfully!")
            agent = WaterIntakeAgent()
            feedback = agent.analyze_intake(intake_ml)
            st.sidebar.write(f"Hydration Status: {feedback}")
        else:
            st.sidebar.error("Please enter a valid User ID before logging intake.")

    st.header("Intake History")
    if user_id:
        history = get_intake_history(user_id)
        if history:
            df = pd.DataFrame(history, columns=["Intake (ml)", "Date"])
            st.dataframe(df)
        else:
            st.info("No intake history found for this user.")
    else:
        st.write("Please enter a User ID to view intake history.")
