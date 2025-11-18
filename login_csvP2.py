import streamlit as st
import pandas as pd
import os
import uuid  # to generate unique user IDs
import re

# setting the DB up
csv_file = "userdatabase.csv"
expected_cols = ["userID", "username", "password"]

# loading the DB
def load_or_fix_user_database(path: str):
    if not os.path.exists(path):
        st.info("Creating new user database...")
        df = pd.DataFrame(columns=expected_cols)
        df.to_csv(path, index=False)
        return df

    try:
        df = pd.read_csv(path)

        # fix if incorrect columns
        if list(df.columns) != expected_cols:
            st.warning("Old or invalid CSV format detected. Fixing it automatically...")
            df = df.iloc[:, :len(expected_cols)]  # trim extra columns
            df.columns = expected_cols[:df.shape[1]]  # rename safely
            df.to_csv(path, index=False)

    except pd.errors.ParserError:
        # recreate good version if bad 
        st.error("Corrupted user database detected. Rebuilding it.")
        df = pd.DataFrame(columns=expected_cols)
        df.to_csv(path, index=False)

    return df

# load user new DB
df = load_or_fix_user_database(csv_file)

# start session
for key in ["logged_in", "username", "userID"]:
    if key not in st.session_state:
        st.session_state[key] = None

# title 
st.title("Login / Signup Page")

# mode switch 
auth_mode = st.radio("Choose mode:", ["Log In", "Sign Up"], index=0)

# login mode
if auth_mode == "Log In":
    st.subheader("Log In") # headers 

    with st.form("login_form"):  # login form 
        login_username = st.text_input("Username", key="login_user")
        login_password = st.text_input("Password", type="password", key="login_pass")
        login_submit = st.form_submit_button("Log In")

    if login_submit:  # when user submits 
        user = df[(df["username"] == login_username) & (df["password"] == login_password)]
        if not user.empty:  # if its there log them in 
            st.session_state["logged_in"] = True
            st.session_state["username"] = user.iloc[0]["username"]
            st.session_state["userID"] = user.iloc[0]["userID"]
            st.success(f"Welcome back, {st.session_state['username']}!")
        else:
            st.error("Invalid username or password.")  # if login/password wrong

# signup mode
elif auth_mode == "Sign Up":
    st.subheader("Sign Up") # header 

    with st.form("signup_form"): # signup form 
        new_username = st.text_input("Choose a username", key="signup_user")
        new_password = st.text_input("Choose a password", type="password", key="signup_pass")
        
        signup_submit = st.form_submit_button("Sign Up")

    if signup_submit: # if user submited 
        if new_username and new_password:
            if len(new_password) < 8:  # checks password lengh 
                st.error("Password must be at least 8 characters long.")
            elif not re.search(r"\d", new_password): # checks number 
                st.error("Password must contain at least one number.")
            elif new_username in df["username"].values: # checks if the username is taken
                st.error("Username already exists. Please choose another.")
            else:  #if password is good 
                user_id = str(uuid.uuid4())
                new_entry = pd.DataFrame(
                    [[user_id, new_username, new_password]],
                    columns=expected_cols   # add to DB
                )
                new_entry.to_csv(csv_file, mode="a", header=False, index=False)
                st.success("Signup successful! You can now log in.")
        else:
            st.error("Please enter both username and password.")

# sidebar 
st.sidebar.header("Session Info")

if st.session_state["logged_in"]: # display userID mainly for testing
    st.sidebar.success(f"Logged in as: {st.session_state['username']}")
    st.sidebar.write(f"User ID: {st.session_state['userID']}")

    if st.sidebar.button("Log out"): #lets the user logout
        for key in ["logged_in", "username", "userID"]:
            st.session_state[key] = None
        st.experimental_rerun()
else:
    st.sidebar.info("Please log in to continue.") # prompts user to login 
