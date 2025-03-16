import streamlit as st
import pandas as pd
import requests
import os
import sys
from dotenv import load_dotenv

# Import custom modules
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from data_loader import fetch_strava_activities
from recommender_system import content_based_recommender
from agents import ai_workout_analyzer, ai_training_planner

# Load environment variables
load_dotenv()

# UI Setup
st.title("🚴‍♂️ AI-Powered Fitness Recommender & Performance Predictor")

# Store refresh tokens per user
if "user_tokens" not in st.session_state:
    st.session_state["user_tokens"] = {}  # Dictionary to store refresh tokens per user

# Read refresh token from URL
query_params = st.query_params.to_dict()
if "refresh_token" in query_params:
    refresh_token = query_params["refresh_token"]
    st.session_state["user_tokens"]["current_user"] = refresh_token  # Store refresh token

# User Choice: Strava API or CSV Upload
option = st.radio("How do you want to import your workout data?", ["Strava API", "Upload CSV"])

df = None  # Initialize empty dataframe

if option == "Strava API":
    st.markdown("[Login with Strava](http://127.0.0.1:5001/login)")
    st.write("Click the link above to log in with Strava.")

    if "user_tokens" in st.session_state and len(st.session_state["user_tokens"]) > 0:
        refresh_token = st.session_state["user_tokens"].get("current_user")

        if refresh_token:
            # st.write(f"✅ Using Refresh Token: `{refresh_token}`")

            with st.spinner("Fetching Strava Data..."):
                df = fetch_strava_activities(refresh_token)

                if df.empty:
                    st.error("❌ No data found. Please check your Strava account.")
                else:
                    st.success("✅ Successfully imported workouts!")
                    # st.write("🔍 DEBUG: Data Loaded")
                    
                    # 🏋️ **Step 1️⃣: Allow User to Choose Activity Type**
                    activity_types = ["All", "Run", "Walk"]
                    selected_activity_type = st.selectbox("Choose Activity Type for Analysis", activity_types)

                    # 🏋️ **Step 2️⃣: Filter Data Based on Activity Type**
                    if selected_activity_type != "All":
                        df = df[df["Activity Type"] == selected_activity_type]

                    # Show filtered data
                    if df.empty:
                        st.warning(f"⚠️ No {selected_activity_type} activities found.")
                    else:
                        st.dataframe(df)  # ✅ Ensure filtered data is displayed properly

elif option == "Upload CSV":
    uploaded_file = st.file_uploader("Upload your Strava CSV file", type=["csv"])
    if uploaded_file:
        df = pd.read_csv(uploaded_file)
        st.success("✅ CSV uploaded successfully!")

        # 🏋️ **Step 1️⃣: Allow User to Choose Activity Type**
        activity_types = ["All", "Run", "Walk"]
        selected_activity_type = st.selectbox("Choose Activity Type for Analysis", activity_types)

        # 🏋️ **Step 2️⃣: Filter Data Based on Activity Type**
        if selected_activity_type != "All":
            df = df[df["Activity Type"] == selected_activity_type]

        # Show filtered data
        if df.empty:
            st.warning(f"⚠️ No {selected_activity_type} activities found.")
        else:
            st.dataframe(df)  # ✅ Ensure filtered data is displayed properly

# ✅ **Step 3️⃣: Run AI Analysis, Training Plan & Recommendations on Filtered Data**
if df is not None and not df.empty:
    # 🏋️ AI Workout Analysis
    st.subheader("📊 AI Workout Analysis")
    
    # User selects an activity type
  
    if st.button("Analyze My Workouts with AI"):
        with st.spinner("Analyzing your workouts..."):
            # Filter the dataset based on the selected activity type
            if selected_activity_type != "All":
                filtered_df = df[df["Activity Type"] == selected_activity_type]
            else:
                filtered_df = df  # Use full dataset
            
            # Check if there's any data left after filtering
            if filtered_df.empty:
                st.warning(f"⚠️ No data found for {selected_activity_type}. Please choose a different activity type.")
            else:
                workout_summary = filtered_df.describe().to_string()
                insights = ai_workout_analyzer(workout_summary, selected_activity_type)  # ✅ Fix: Now correctly passes two arguments
                st.success("✅ AI Analysis Complete!")
                st.write(insights)


    # 🏆 AI Training Plan Generator
    st.subheader("🏋️ AI-Powered Training Plan")
    goal = st.text_input("Enter your fitness goal (e.g., Improve 5K time, Build endurance, Train for a marathon)")

    if st.button("Generate My AI Training Plan"):
        if goal:
            with st.spinner("Creating your personalized training plan..."):
                training_plan = ai_training_planner(goal, selected_activity_type)  # ✅ Pass activity type
                st.success("✅ Training Plan Generated!")
                st.write(training_plan)
        else:
            st.warning("⚠️ Please enter a goal before generating a training plan.")



    # 🏅 Personalized Workout Recommendations
if st.button("Get My Workout Recommendations"):
    with st.spinner("Generating recommendations..."):
        recommended_cbf = content_based_recommender(df, selected_activity_type, top_n=5)  # ✅ Pass selected type

    if not recommended_cbf.empty:
        st.subheader(f"🏅 Content-Based Recommendations for {selected_activity_type}")
        st.dataframe(recommended_cbf)


st.write("📢 Select how you want to import your workout data and proceed!")
