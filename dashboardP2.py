import streamlit as st
import pandas as pd

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



# Set page title
st.title("Dashboard")

# gets the userID
user_id = st.session_state.get("userID", None)

if user_id is None: # if not loged in say to log in 
    st.error("Please log in")
else:
    try:
        df = pd.read_csv("compound_exercises.csv")  # reads the database 
        user_df = df[df["userID"] == user_id]  # only looks at the current user
        
        if user_df.empty:
            st.info("Please first record a workout")  # if the user has not entered data
        else:
            # pandas data validation for the numbers
            user_df["weight"] = pd.to_numeric(user_df["weight"], errors="coerce")
            user_df["reps"] = pd.to_numeric(user_df["reps"], errors="coerce")
            user_df["sets"] = pd.to_numeric(user_df["sets"], errors="coerce")
            
            # dont use the data that is not valid 
            user_df = user_df.dropna(subset=["weight", "reps", "sets"])
            
            # caculates the total volume per exercises per day(weight*reps*sets)
            user_df["volume"] = user_df["weight"] * user_df["reps"] * user_df["sets"]

            # pandas converts the date into datetime 
            user_df["date"] = pd.to_datetime(user_df["date"], errors="coerce")
            user_df = user_df.dropna(subset=["date"]).sort_values("date")
            
            # only want the compound exercises not the outhers
            user_df["exercise"] = user_df["exercise"].str.lower().str.strip() # data validation
            exercises = ["bench press", "squat", "deadlift"]
            user_df = user_df[user_df["exercise"].isin(exercises)]
            user_df["exercise"] = user_df["exercise"].str.title()  # sets the title
            
            if user_df.empty:
                st.error("No data found for Bench Press, Squat, or Deadlift.") # error message
            else:
                # groups data by date and exercise, sum volume ( if there is more than 1 entey per day )
                grouped = user_df.groupby(["date", "exercise"])["volume"].sum().reset_index()               
                pivot_df = grouped.pivot(index="date", columns="exercise", values="volume").fillna(0)
                
                # Display the plot
                st.subheader("Volume Per Exercise Over Time")
                st.line_chart(pivot_df) # displays sported data
                st.divider()
                st.markdown("Testing data")
                # testing only bellow
                with st.expander("View data"):
                    st.dataframe(user_df)
                # testing only above 
    
    except FileNotFoundError:
        st.error("File not found")
    except Exception as e:
        st.error(f"An error occurred: {str(e)}")

import streamlit as st
import random
import pandas as pd
import ast



df = pd.read_csv("workouts.csv")   # opens the csv file
last_row = df.tail(1).iloc[0]      # pickes the last row 
sport = last_row["Sport"]       # gets the sport value from file and store as a var 
position = last_row["Position"]
muscle_focus = last_row["Muscle Focus"]
weekTemplate = [day.strip() for day in last_row["Workout Days"].split(",")] # gets the days array from csv and stors it as an array  
equipment = [eq.strip() for eq in last_row["Equipment"].split(",")]   # the .split  makes it so it does not output as [m,o,n,d,a,y]
volume = last_row["Volume"]
plan_lengh = last_row["Plan Length"]
fitness_level = last_row["Fitness Level"]
workout_duration = last_row["Workout Duration"]
intensity = last_row["Intensity"]


chest = 10  # sets the starting values 
arms = 10
legs = 10
core = 10
back = 10


# big dictionary with 10 workouts for each muscle group and repeates for each pice of equipment
# naming convention is exersise_exersises_muscle
exercise_pool = {


    "dembbell_exersises_arms": [
        "Dumbbell Bicep Curl",
        "Hammer Curl",
        "Concentration Curl",
        "Zottman Curl",
        "Incline Dumbbell Curl",
        "Cross Body Hammer Curl",
        "Dumbbell Reverse Curl",
        "Overhead Dumbbell Tricep Extension",
        "Dumbbell Tricep Kickback",
        "Dumbbell Skull Crushers"
    ],
    
    "dembbell_exersises_back": [
        "Dumbbell Bent Over Row",
        "Renegade Row (with dumbbells)",
        "Single Arm Dumbbell Row",
        "Incline Dumbbell Row",
        "Dumbbell Deadlift",
        "Dumbbell Shrugs",
        "Dumbbell High Pull",
        "Dumbbell Pullover (lat-focused)",
        "Seal Row with Dumbbells",
        "Dumbbell Reverse Fly (for rear delts and upper back)"
    ],

    "dembbell_exersises_legs": [
        "Dumbbell Goblet Squat",
        "Dumbbell Romanian Deadlift",
        "Dumbbell Bulgarian Split Squat",
        "Dumbbell Step-Ups",
        "Dumbbell Sumo Squat",
        "Dumbbell Front Squat",
        "Dumbbell Walking Lunge",
        "Dumbbell Calf Raise",
        "Dumbbell Glute Bridge (with dumbbell on hips)",
        "Dumbbell Side Lunge"
    ],
    "dembbell_exersises_core": [
        "Dumbbell Russian Twist",
        "Dumbbell Side Bend",
        "Dumbbell Sit-Up (holding dumbbell)",
        "Dumbbell Leg Raise (with dumbbell between feet or on ankles)",
        "Dumbbell Woodchopper",
        "Dumbbell Dead Bug",
        "Dumbbell V-Up",
        "Dumbbell Weighted Crunch",
        "Dumbbell Standing Oblique Crunch",
        "Dumbbell Plank Row (Renegade Row with core focus)"
    ],
    "dembbell_exersises_chest": [
        "Dumbbell Bench Press",
        "Dumbbell Chest Fly",
        "Dumbbell Incline Press",
        "Dumbbell Pullover (chest-focused)",
        "Dumbbell Shoulder Press",
        "Dumbbell Arnold Press",
        "Dumbbell Lateral Raise",
        "Dumbbell Front Raise",
        "Dumbbell Upright Row",
        "Dumbbell Reverse Fly (rear delts)"

    ],

    # all the body weight exercises
    "bodyweight_exercises_arms": [
        "Diamond Push-Up",
        "Close-Grip Push-Up",
        "Triceps Dip (on bench or chair)",
        "Isometric Arm Hold",
        "Wall Push-Up",
        "Incline Push-Up",
        "Pseudo Planche Push-Up",
        "Arm Circles",
        "Pike Push-Up (triceps focus)",
        "Push-Up to Arm Reach"
    ],
    "bodyweight_exercises_back": [

        "Superman Hold",
        "Superman Pull",
        "Reverse Snow Angels",
        "Wall Angels",
        "Bird-Dog",
        "Quadruped Arm/Leg Raise",
        "Bridge with Arm Reach",
        "Prone Y-T-I Raises",
        "Table Bridge",
        "Doorway Row (if allowed as bodyweight)"
    ],
    "bodyweight_exercises_legs": [
        "Bodyweight Squat",
        "Lunges",
        "Wall Sit",
        "Step-Ups (on stairs or bench)",
        "Bulgarian Split Squat (using a chair)",
        "Glute Bridge",
        "Calf Raises",
        "Jump Squats",
        "Side Lunges",
        "Single-Leg Glute Bridge"

    ],
    "bodyweight_exercises_core": [
        "Plank",
        "Side Plank",
        "Crunches",
        "Leg Raises",
        "Bicycle Crunches",
        "Mountain Climbers",
        "V-Ups",
        "Flutter Kicks",
        "Toe Touches",
        "Dead Bug"
    ],
    "bodyweight_exercises_chest": [
        "Push-Up",
        "Incline Push-Up",
        "Decline Push-Up",
        "Wide Push-Up",
        "Pike Push-Up (shoulder focus)",
        "Wall Walk",
        "Shoulder Tap Push-Up",
        "Archer Push-Up",
        "Dive Bomber Push-Up",
        "Handstand Hold (against wall)"
    ],

    # all the reistance band exercises
    "band_exercises_arms": [
        "Resistance Band Bicep Curl",
        "Resistance Band Hammer Curl",
        "Resistance Band Concentration Curl",
        "Resistance Band Reverse Curl",
        "Resistance Band Overhead Tricep Extension",
        "Resistance Band Tricep Kickback",
        "Resistance Band Crossbody Curl",
        "Resistance Band Zottman Curl",
        "Resistance Band Tricep Pushdown (anchored)",
        "Resistance Band Preacher Curl (anchored)"
    ],
    "band_exercises_back": [
        "Resistance Band Seated Row",
        "Resistance Band Bent Over Row",
        "Resistance Band Lat Pulldown (anchored overhead)",
        "Resistance Band Face Pull",
        "Resistance Band Straight Arm Pulldown",
        "Resistance Band Deadlift",
        "Resistance Band Reverse Fly",
        "Resistance Band Shrugs",
        "Resistance Band Archer Row",
        "Resistance Band Good Morning"
    ],
    "band_exercises_legs": [
        "Resistance Band Squat",
        "Resistance Band Deadlift",
        "Resistance Band Glute Bridge (band around thighs)",
        "Resistance Band Lateral Walk",
        "Resistance Band Standing Leg Curl",
        "Resistance Band Kickback",
        "Resistance Band Step-Out Squat",
        "Resistance Band Front Squat (band under feet)",
        "Resistance Band Standing Hip Abduction",
        "Resistance Band Bulgarian Split Squat (band under front foot)"
    ],
    "band_exercises_core": [
        "Resistance Band Russian Twist",
        "Resistance Band Woodchopper",
        "Resistance Band Seated Ab Crunch",
        "Resistance Band Bicycle Twist",
        "Resistance Band Standing Oblique Crunch",
        "Resistance Band Dead Bug",
        "Resistance Band Pallof Press",
        "Resistance Band Side Bend",
        "Resistance Band Toe Touch",
        "Resistance Band Plank Row (band anchored)"
    ],
    "band_exercises_chest": [
        "Resistance Band Chest Press",
        "Resistance Band Chest Fly",
        "Resistance Band Incline Chest Press",
        "Resistance Band Decline Chest Press",
        "Resistance Band Shoulder Press",
        "Resistance Band Lateral Raise",
        "Resistance Band Front Raise",
        "Resistance Band Upright Row",
        "Resistance Band Rear Delt Fly",
        "Resistance Band Arnold Press"
    ],

    # all the free weight exercises
    "free_exercises_arms": [
        "Barbell Curl",
        "EZ Bar Curl",
        "Barbell Reverse Curl",
        "Barbell Skull Crushers",
        "EZ Bar Preacher Curl",
        "Barbell Wrist Curl",
        "Barbell Overhead Tricep Extension",
        "Close-Grip Barbell Bench Press",
        "Kettlebell Curl",
        "Kettlebell Overhead Tricep Extension"
    ],
    "free_exercises_back": [
        "Barbell Bent Over Row",
        "Pendlay Row",
        "T-Bar Row (with barbell)",
        "Barbell Deadlift",
        "Kettlebell Renegade Row",
        "Barbell Shrugs",
        "Kettlebell High Pull",
        "Kettlebell Suitcase Deadlift",
        "Barbell Seal Row",
        "Kettlebell Bent Over Row"
    ],
    "free_exercises_legs": [
        "Barbell Back Squat",
        "Barbell Front Squat",
        "Barbell Romanian Deadlift",
        "Barbell Hip Thrust",
        "Barbell Sumo Deadlift",
        "Kettlebell Swing",
        "Kettlebell Goblet Squat",
        "Kettlebell Step-Up",
        "Kettlebell Bulgarian Split Squat",
        "Barbell Walking Lunge"
    ],
    "free_exercises_core": [
        "Barbell Rollout",
        "Barbell Landmine Twist",
        "Kettlebell Windmill",
        "Kettlebell Turkish Get-Up",
        "Kettlebell Russian Twist",
        "Barbell Overhead Carry",
        "Kettlebell Side Bend",
        "Barbell Weighted Sit-Up",
        "Kettlebell Halo",
        "Barbell Standing Oblique Crunch"
    ],

    "free_exercises_chest": [
        "Barbell Bench Press",
        "Incline Barbell Bench Press",
        "Barbell Overhead Press",
        "Barbell Push Press",
        "Barbell Upright Row",
        "Barbell Floor Press",
        "Kettlebell Floor Press",
        "Kettlebell Clean and Press",
        "Kettlebell Arnold Press",
        "Barbell Incline Close-Grip Press"
    ],

    # all the machine/cable exercises
    "machine_exercises_arms": [
        "Cable Bicep Curl",
        "Cable Hammer Curl (with rope attachment)",
        "Cable Concentration Curl",
        "Cable Reverse Curl",
        "Cable Overhead Tricep Extension",
        "Cable Tricep Pushdown (with bar or rope)",
        "Cable Kickback",
        "Preacher Curl Machine",
        "Tricep Extension Machine",
        "Cable Zottman Curl"
    ],
    "machine_exercises_back": [
        "Lat Pulldown (cable machine)",
        "Seated Cable Row",
        "Cable Straight Arm Pulldown",
        "Cable Face Pull",
        "Assisted Pull-Up Machine",
        "Back Extension Machine",
        "Cable Reverse Fly",
        "Cable Shrugs",
        "Cable High Row",
        "Cable Lat Sweep Row"
    ],
    "machine_exercises_legs": [
        "Leg Press Machine",
        "Leg Curl Machine (seated or lying)",
        "Leg Extension Machine",
        "Cable Kickback (glutes)",
        "Cable Standing Hamstring Curl",
        "Cable Side Leg Raise",
        "Cable Front Leg Raise",
        "Hip Abduction Machine",
        "Hip Adduction Machine",
        "Glute Kickback Machine"
    ],
    "machine_exercises_core": [
        "Cable Woodchopper",
        "Cable Standing Oblique Crunch",
        "Cable Kneeling Crunch",
        "Cable Pallof Press",
        "Ab Crunch Machine",
        "Rotary Torso Machine",
        "Cable Side Bend",
        "Cable Reverse Crunch (with ankle strap)",
        "Cable Dead Bug",
        "Cable Seated Twist"
    ],
    "machine_exercises_chest": [
        "Cable Chest Press",
        "Cable Chest Fly",
        "Cable Incline Chest Fly",
        "Cable Crossover",
        "Pec Deck Machine",
        "Shoulder Press Machine",
        "Cable Lateral Raise",
        "Cable Front Raise",
        "Cable Upright Row",
        "Reverse Pec Deck (rear delts)"
    ]
}




# gives values based on what sport you play

if sport == "rugby":
    if position == "forward":  # e.g. if you a forward more focus is on back and legs
        chest = chest + 4
        back = back + 8
        arms = arms + 8
        core = core + 2
        legs = legs + 7
        
    elif position == "back":
        chest = chest + 5
        back = back + 2
        arms = arms + 5 
        core = core + 3
        legs = legs + 7

elif sport == "football":
    if position == "defender":
        chest = chest + 6
        back = back + 5
        arms = arms + 4
        core = core + 6
        legs = legs + 10
    elif position == "midfielder":
        chest = chest + 4
        back = back + 4
        arms = arms + 3
        core = core + 5
        legs = legs + 10
    elif position == "forward":
        chest = chest + 3
        back = back + 3
        arms = arms + 2
        core = core + 4
        legs = legs + 8

elif sport == "tennis":
    if position == "aggressive":
        chest = chest + 8
        back = back + 4
        arms = arms + 8
        core = core + 6
        legs = legs + 4
        
    elif position == "defensive":
        chest = chest + 7
        back = back + 5
        arms = arms + 7
        core = core + 5
        legs = legs + 5

elif sport == "track":
    if position == "feild":
        chest = chest + 4
        back = back + 4
        arms = arms + 4
        core = core + 6
        legs = legs + 10
    elif position == "track":
        chest = chest + 2
        back = back + 5
        arms = arms + 4
        core = core + 5
        legs = legs + 10
    

elif sport == "golf":
    if position == "safe":
        chest = chest + 15
        back = back + 5
        arms = arms + 10
        core = core + 5
        legs = legs + 5
    elif position == "risky":
        chest = chest + 5
        back = back + 10
        arms = arms + 5
        core = core + 8
        legs = legs + 15
    elif PowerPos == "balanced":
        chest = chest + 6
        back = back + 15    
        arms = arms + 8
        core = core + 10
        legs = legs + 10

elif sport == "basketball" :
    if position == "shooting":
        chest = chest + 8
        back = back + 5
        arms = arms + 7
        core = core + 8
        legs = legs + 10

    elif position == "power":
        chest = chest + 8
        back = back + 7
        arms = arms + 4
        core = core + 6
        legs = legs + 10


if muscle_focus == "chest" :  # when the user gave a muscle they wanted to fucus on more it does that  
    chest = chest + 12
elif muscle_focus == "back" :
    back = back + 12
elif muscle_focus == "arms" :
    arms = arms + 12
elif muscle_focus == "core" :
    core = core + 12 
elif muscle_focus == "legs" :
    legs = legs + 12



# Calculate total
total = chest + arms + legs + core + back

# rounds the ratios 
def round_sf(value, sig_figs):
    return float(f"{value:.{sig_figs}g}")

chest_ratio = round_sf(chest / total, 2) # creates the ratios 
arms_ratio = round_sf(arms / total, 2)
legs_ratio = round_sf(legs / total, 2)
core_ratio = round_sf(core / total, 2)
back_ratio = round_sf(back / total, 2)

with st.expander("Show peramiters"): 
#if st.button("Show peramiters"):   # shows the users previously imputed peramites (testing)
    st.markdown(f"Sport: {sport}")
    st.markdown(f"Position: {position}")
    st.markdown(f"Muscle Focus: {muscle_focus}")
    st.markdown(f"Days: {weekTemplate}")
    st.markdown(f"Equipment: {equipment}")
    # output results
    st.markdown(f"Chest Ratio: {chest_ratio}")
    st.markdown(f"Arms Ratio: {arms_ratio}")
    st.markdown(f"Legs Ratio: {legs_ratio}")
    st.markdown(f"Core Ratio: {core_ratio}")
    st.markdown(f"Back Ratio: {back_ratio}")
    st.markdown(f"Intensity: {intensity}")
    st.markdown(f"Fitness level: {fitness_level}")
    st.markdown(f"Workout duration: {workout_duration}")
    st.markdown(f"Volume: {volume}")

# the finctiong that creates the workouts based on the ratios and days they can train
def generate_workout_schedule(
    chest_ratio, arms_ratio, legs_ratio, core_ratio, back_ratio,
    equipment, exercise_pool, weekTemplate
):
    used_exercises = set()
    
    # i want 8 exersises per day but this will change in layter versions (so future proofing it)
    def get_exercises(volume,fitness_level,workout_duration,intensity):
        exercises = 0

        if volume == "Very low":
            exercises = exercises + 1
        elif volume == "Low":
            exercises = exercises + 2
        elif volume == "Medium":
            exercises = exercises + 3
        elif volume == "High":
            exercises = exercises + 4
        elif volume == "Very high":
            exercises = exercises + 5
        else:
            exercises = exercises + 3


        if fitness_level == "Very low":
            exercises = exercises + 1
        elif fitness_level == "Low":
            exercises = exercises + 2
        elif fitness_level == "Medium":
            exercises = exercises + 3
        elif fitness_level == "High":
            exercises = exercises + 4
        elif fitness_level == "Very high":
            exercises = exercises + 5
        else:
            exercises = exercises + 3

        

        if workout_duration == "Very short":
            exercises = exercises + 1
        elif workout_duration == "Short":
            exercises = exercises + 2
        elif workout_duration == "Medium":
            exercises = exercises + 3
        elif workout_duration == "Long":
            exercises = exercises + 4
        elif workout_duration == "Very long":
            exercises = exercises + 5
        else:
            exercises = exercises + 3

        

        if intensity == "Very low":
            exercises = exercises + 1
        elif intensity == "Low":
            exercises = exercises + 2
        elif intensity == "Medium":
            exercises = exercises + 3
        elif intensity == "High":
            exercises = exercises + 4
        elif intensity == "Very high":
            exercises = exercises + 5
        else:
            exercises = exercises + 3

        

        if exercises == 4 or exercises == 5 or exercises == 6:
            total_exercises_per_day = 5
        if exercises == 7 or exercises == 8 or exercises == 9:
            total_exercises_per_day = 6
        if exercises == 10 or exercises == 11 or exercises == 12:
            total_exercises_per_day = 7
        if exercises == 13 or exercises == 14 or exercises == 15:
            total_exercises_per_day = 8
        if exercises == 16 or exercises == 17 or exercises == 18:
            total_exercises_per_day = 9
        if exercises == 19 or exercises == 20 :
            total_exercises_per_day = 10


        return(total_exercises_per_day)

    total_exercises_per_day = get_exercises(volume,fitness_level,workout_duration,intensity)

    # defines the muscle ratios
    muscle_ratios = {
        "chest": chest_ratio,
        "arms": arms_ratio,
        "legs": legs_ratio,
        "core": core_ratio,
        "back": back_ratio
    }

    # creates the workout for 1 day 
    for day in weekTemplate:   # loops through all workouts days the user want to change 
        st.header(f" {day} workout") # prints the day and then workout so you can see how each relates 

        # decides the number of exercuses per muscle using the ratios 
        muscle_counts = {}
        remaining = total_exercises_per_day
        # 
        for muscle, ratio in muscle_ratios.items(): # loops through the muscle grops and the ratios
            count = round(ratio * total_exercises_per_day) # calcs how many each sould get rounds to insure the correct amount 
            muscle_counts[muscle] = count  # store is the dictonary
            remaining -= count  # updates the count 

        # makes sure there is enough due to the rounding
        muscles_sorted = sorted(muscle_ratios.items(), key=lambda x: x[1], reverse=True)
        i = 0
        while remaining > 0:  # if there are some remaining then add a exercise 
            muscle = muscles_sorted[i % len(muscles_sorted)][0]
            muscle_counts[muscle] += 1  # updates the count
            remaining -= 1
            i += 1 

        day_plan = [] # creates the array 

        for muscle, count in muscle_counts.items():  # start looping muscle counts
            selected = 0  # create the vars 
            attempts = 0

            while selected < count and attempts < 100:   # to avoid the program getting stuck
                equip = random.choice(equipment)   # randomly picks one out of the ones its allowed too

    
                pool_key = f"{equip}_exercises_{muscle}" # creates the key to use for the dictonary 

                if pool_key in exercise_pool:  # see if the equipment and muscle are there 
                    choices = list(set(exercise_pool[pool_key]) - used_exercises)  # gets rid of duplicated exercises

                    if choices:  # if theres a duplicate it randomly picks anouther
                        exercise = random.choice(choices)
                        used_exercises.add(exercise)  

                        reps = random.randint(4, 12)  # randomly picks an amount of reps and sets for exach exercise 
                        sets = random.randint(2, 4)

                        day_plan.append({
                            "Muscle Group": muscle.capitalize(),
                            "Exercise": exercise,
                            "Equipment": equip.capitalize(),
                            "Sets": sets,
                            "Reps": reps
                        })  # adds in the row of data into the day plan

                        selected += 1  # updates the count 
                attempts += 1 # updates the count
        
        # displays the table 
        df_day = pd.DataFrame(day_plan)
        st.table(df_day)





# calls the function 
st.markdown("---")
st.markdown("Generate workout plan")  # addes the text 

with st.expander("Generate Workouts"):  # if the button is pressed runs the function to generate workouts
    generate_workout_schedule(
        chest_ratio, arms_ratio, legs_ratio, core_ratio, back_ratio,
        equipment, exercise_pool, weekTemplate
    )

if st.button("Regenerate workout plan"):
    generate_workout_schedule(
        chest_ratio, arms_ratio, legs_ratio, core_ratio, back_ratio,
        equipment, exercise_pool, weekTemplate
    )
