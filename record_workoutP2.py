import streamlit as st
import pandas as pd
from datetime import date
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


st.set_page_config(page_title="Workout Recorder", layout="centered")

# --- USER LOGIN CHECK ---
if "userID" not in st.session_state or not st.session_state["userID"]:
    st.warning("Please log in first.")
    st.stop()

user_id = st.session_state["userID"]
username = st.session_state.get("username", "Unknown User")

st.title("Workout Recorder")
st.caption(f"Logged in as **{username}** (User ID: {user_id})")

# --- CHOOSE MODE ---
auth_mode = st.radio("Choose mode:", ["Compound", "Other"], index=0)

# --- FILE PATHS ---
compound_file = "compound_exercises.csv"
other_file = "other_exercises.csv"

# --- ENSURE CSV FILES EXIST ---
for f in [compound_file, other_file]:
    if not os.path.exists(f):
        pd.DataFrame(columns=["userID", "date", "exercise", "weight", "reps", "sets"]).to_csv(f, index=False)

# --- ADD COMPOUND EXERCISES ---
if auth_mode == "Compound":
    st.header("Add Compound Exercise")

    exercise_options = ["Bench Press", "Squat", "Deadlift"]
    with st.form("compound_form"):
        exercise = st.selectbox("Select an Exercise", exercise_options)
        weight = st.number_input("Weight (kg)", min_value=0.0, step=0.5)
        reps = st.number_input("Reps", min_value=1, step=1)
        sets = st.number_input("Sets", min_value=1, step=1)
        submitted = st.form_submit_button("Add Entry")

    if submitted:
        new_entry = pd.DataFrame([{
            "userID": user_id,
            "date": date.today(),
            "exercise": exercise,
            "weight": weight,
            "reps": reps,
            "sets": sets
        }])
        df = pd.read_csv(compound_file)
        df = pd.concat([df, new_entry], ignore_index=True)
        df.to_csv(compound_file, index=False)
        st.success(f"Added {exercise} — {weight} kg × {reps} reps × {sets} sets")

# --- ADD OTHER EXERCISES ---
elif auth_mode == "Other":
    st.header("Add Other Exercise")

    with st.form("other_form"):
        exercise = st.text_input("Exercise name")
        weight = st.number_input("Weight (kg)", min_value=0.0, step=0.5)
        reps = st.number_input("Reps", min_value=1, step=1)
        sets = st.number_input("Sets", min_value=1, step=1)
        submitted = st.form_submit_button("Add Entry")

    if submitted:
        if exercise.strip() == "":
            st.error("Please enter a valid exercise name.")
        else:
            new_entry = pd.DataFrame([{
                "userID": user_id,
                "date": date.today(),
                "exercise": exercise.strip(),
                "weight": weight,
                "reps": reps,
                "sets": sets
            }])
            df = pd.read_csv(other_file)
            df = pd.concat([df, new_entry], ignore_index=True)
            df.to_csv(other_file, index=False)
            st.success(f"Added {exercise} — {weight} kg × {reps} reps × {sets} sets")

# --- DISPLAY DATABASES AT THE BOTTOM ---
st.markdown("---")
st.subheader("Workout Databases")

# Load both CSVs
compound_df = pd.read_csv(compound_file)
other_df = pd.read_csv(other_file)

# Filter only the logged-in user's data
compound_user_df = compound_df[compound_df["userID"] == user_id]
other_user_df = other_df[other_df["userID"] == user_id]

# Display user-only compound exercises
with st.expander("Your Compound Exercises", expanded=False):
    if not compound_user_df.empty:
        st.dataframe(compound_user_df.sort_values(by="date", ascending=False))
    else:
        st.info("No compound exercises recorded yet.")

# Display user-only other exercises
with st.expander("Your Other Exercises", expanded=False):
    if not other_user_df.empty:
        st.dataframe(other_user_df.sort_values(by="date", ascending=False))
    else:
        st.info("No other exercises recorded yet.")

# Optional: show full database for debugging/admin
with st.expander("Full Databases (All Users)"):
    st.write("**Compound Exercises (All Users)**")
    st.dataframe(compound_df)
    st.write("**Other Exercises (All Users)**")
    st.dataframe(other_df)

    st.dataframe(other_df)
