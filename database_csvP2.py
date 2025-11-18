import streamlit as st
import pandas as pd
import os





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





