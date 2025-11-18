import streamlit as st
import pandas as pd
import os
import csv

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



csv_file = "workouts.csv"  # define the csv file 
columns = [
    "Sport", "Position", "Muscle Focus", "Workout Days", "Intensity",
    "Priority", "Fitness Level", "Plan Length", "Workout Type",
    "Workout Duration", "Weight", "Height", "Equipment", "Wish", "Volume"
]

if os.path.exists(csv_file):
    # Migrate the CSV to handle column changes
    rows = []
    with open(csv_file, 'r', newline='') as f:
        reader = csv.reader(f)
        for row in reader:
            rows.append(row)
    if rows:
        data_rows = rows[1:] if len(rows) > 0 else []
        for row in data_rows:
            while len(row) < len(columns):
                row.append('')
            if len(row) > len(columns):
                row[:] = row[:len(columns)]  # truncate if extra
        rows = [columns] + data_rows
        with open(csv_file, 'w', newline='') as f:
            writer = csv.writer(f)
            writer.writerows(rows)

if not os.path.exists(csv_file):         # if the file does not exist it will make one 
    pd.DataFrame(columns=columns).to_csv(csv_file, index=False)

st.header("Generate workout")        # creates the top header 
st.markdown("This is the generate workout function. You answer questions to help the algorithm make a custom workout")
st.divider()  # adds a line to separate for ease of reading 

sport = st.selectbox("What sport do you play?", ["rugby", "football", "tennis", "track", "golf", "basketball"])  # first input outside the form since it is conditional 

with st.form("workout_form"):   # inputs what sport the user plays based on what sport they play (also is the start of the form)
    if sport == "rugby":
        position = st.radio("What position do you play?", ["forward", "back"]) # asks the user what position they are in the previously inputted sport   
    elif sport == "football":
        position = st.radio("What position do you play?", ["forward", "midfield", "defender"])
    elif sport == "tennis":
        position = st.radio("What style do you play?", ["defensive", "aggressive"])
    elif sport == "track":
        position = st.radio("What type of athlete are you?", ["field", "track"])
    elif sport == "golf":
        position = st.radio("What is your play style?", ["safe", "risky"])
    elif sport == "basketball":
        position = st.radio("What role do you play?", ["power", "shooting"])

    muscle_focus = st.selectbox("What muscle do you want to focus on?", ["arms", "chest & shoulders", "legs", "back", "core"]) # selectbox multiple inputs per question 
    workout_days = st.multiselect("What days do you want your workouts to be on?", ["monday", "tuesday", "wednesday", "thursday", "friday", "saturday", "sunday"])
    intensity = st.select_slider("How intense do you want to train?", ["Very low", "Low", "Medium", "High", "Very high"])
    priority = st.selectbox("What is your main priority?", ["build muscle", "get stronger", "maximize strength", "general health", "fat loss"])
    fitness_level = st.select_slider("What is your current fitness level?", ["Very low", "Low", "Medium", "High", "Very high"])
    plan_length = st.select_slider("How many weeks long do you want your plan to be?", ["4", "6", "8", "10", "12"])  # allows user to select number with a slider 
    workout_type = st.selectbox("What is your preferred workout type?", ["weightlifting", "cardio", "HIIT", "calisthenics", "choose for me"])
    workout_duration = st.select_slider("How long do you want the workout to be?", ["Very short", "Short", "Medium", "Long", "Very Long"])
    weight = st.select_slider("How much do you weigh (Kg)?", [str(i) for i in range(30, 181, 1)])
     # above line - rather than writing each option loops iteratively rather than writing out all the options in an array
    height = st.select_slider("How tall are you (cm)?", [str(i) for i in range(120, 261, 1)])
    equipment = st.multiselect("What equipment do you have access to?", ["free ", "machine", "dumbbells", "band"])
    wish = st.selectbox("What is one thing you wish you had more of in your current workouts?", ["Variety", "Intensity", "Structure", "Recovery", "Fun"])
    volume = st.select_slider("How much volume do you want in your workouts?", ["Very low", "Low", "Medium", "High", "Very high"])

    submitted = st.form_submit_button("Submit")   # allows the user to submit the form

    if submitted:
        st.success("Form submitted") # if it works displays message to confirm (helps with testing)
        st.write("choices = ")
        st.write(sport, position, muscle_focus, workout_days, intensity, priority, fitness_level, plan_length, workout_type, workout_duration, weight, height, equipment, wish, volume)
        # line above displays the users inputs ( mainly for testing )
        # line below creates a new line and all the vars and arrays are columns for the database  
        new_entry = pd.DataFrame([[
            sport, position, muscle_focus, ",".join(workout_days), intensity,
            priority, fitness_level, plan_length, workout_type,
            workout_duration, weight, height, ",".join(equipment), wish, volume
        ]], columns=columns)

        new_entry.to_csv(csv_file, mode='a', header=False, index=False) # saves data to the file 
        st.success("Saved") # if it works displays the message(helps with testing)

st.divider()  # divider helps to break up the next section 
st.subheader("Saved workouts")   # creates a sub header 

if st.button("Show workouts"):   # when the button is pressed 
    df = pd.read_csv(csv_file)   # opens file to read it 
    if not df.empty:            # if its not empty 
        st.dataframe(df, use_container_width=True)  # displays the database using the streamlit library  
    else:
        st.markdown("Error no saved workouts")          # if there is no data displays message 
