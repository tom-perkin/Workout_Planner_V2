import streamlit as st
import pandas as pd
import os

# --- SIDEBAR INFO ---
st.sidebar.header("Session Info")

if st.session_state["logged_in"]:
    st.sidebar.success(f"Logged in as: {st.session_state['username']}")
    st.sidebar.write(f"User ID: {st.session_state['userID']}")
    if st.sidebar.button("Log out"):
        for key in ["logged_in", "username", "userID"]:
            st.session_state[key] = None
        st.experimental_rerun()
else:
    st.sidebar.info("Please log in to continue.")

# ------------------------------------------------------------------
#  AUTHORIZATION CHECK – ONLY ALLOW SPECIFIC USER ID
# ------------------------------------------------------------------
ALLOWED_USER_ID = "d7933cee-fac7-48c7-a35a-f6ac2dbc8f85"

# Streamlit Cloud (and newer Streamlit versions) injects the user info
# via environment variables when "Email authentication" is enabled in app settings
def get_current_user_id() -> str | None:
    # Method 1: Streamlit Cloud with authentication turned on
    user_info = st.experimental_user
    if user_info and "user_id" in user_info:
        return user_info["user_id"]

    # Method 2: Fallback for some older deployments / custom auth
    email = st.experimental_user.get("email")
    if email:
        # Create a deterministic ID from the email (same way Streamlit does internally)
        return hashlib.sha256(email.lower().encode()).hexdigest()

    return None

current_user_id = get_current_user_id()

if current_user_id != ALLOWED_USER_ID:
    st.error("🚫 Access denied")
    st.info("This page is private and only visible to the authorized user.")
    st.stop()  # Stops execution – nothing below this will be shown

st.set_page_config(page_title="Workout Recorder", layout="centered")

# --- USER LOGIN CHECK ---
if "userID" not in st.session_state or not st.session_state["userID"]:
    st.warning("Please log in first.")
    st.stop()

user_id = st.session_state["userID"]
username = st.session_state.get("username", "Unknown User")

st.title("Workout Recorder")
st.caption(f"Logged in as **{username}** (User ID: {user_id})")




st.set_page_config(page_title="Database", layout="wide")
page_bg = """
<style>
    .stApp {
        background-color: #6bcde8; /* light blue */
    }
</style>
"""
st.markdown(page_bg, unsafe_allow_html=True)












st.title("Databases")
st.markdown("this is for me only")
st.divider()
st.header("User database")

user_csv = "userdatabase.csv"
if not os.path.exists(user_csv):
    pd.DataFrame(columns=["username", "password"]).to_csv(user_csv, index=False)

user_df = pd.read_csv(user_csv)
edited_user_df = st.data_editor(user_df, num_rows="dynamic")
if st.button("Save User Changes"):
    edited_user_df.to_csv(user_csv, index=False)
    st.success("User changes saved to CSV!")

st.divider()
st.header("Workout database")

workout_csv = "workouts.csv"
if not os.path.exists(workout_csv):
    pd.DataFrame(columns=[
        "Sport", "Position", "Muscle Focus", "Workout Days", "Intensity",
        "Priority", "Fitness Level", "Plan Length", "Workout Type",
        "Workout Duration", "Weight", "Height", "Equipment", "Wish"
    ]).to_csv(workout_csv, index=False)

workout_df = pd.read_csv(workout_csv)
edited_workout_df = st.data_editor(workout_df, num_rows="dynamic", use_container_width=True)
if st.button("Save Workout Changes"):
    edited_workout_df.to_csv(workout_csv, index=False)
    st.success("Workout changes saved to CSV!")

#####





