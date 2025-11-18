import streamlit as st

#put the header here 
pages = {
    "Your account": [
        st.Page("login_csvP2.py", title="Login/Signup"),
        st.Page("GenerateWorkout2_csvP2.py", title="Questions page"),
        st.Page("dashboardP2.py", title="Dashboard"),
        # st.Page("recordP2V3.py", title="Generate Workouts"),
        st.Page("record_workoutP2.py", title="Record workout"),
        st.Page("database_csvP2.py", title="Databases (Admin)"),

    ],
}


pg = st.navigation(pages)
pg.run()


