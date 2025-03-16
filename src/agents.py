import os
import pandas as pd
import google.generativeai as genai
from dotenv import load_dotenv

# Load API key
load_dotenv()
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
genai.configure(api_key=GEMINI_API_KEY)

import google.generativeai as genai  # ✅ Correct Import

def ai_workout_analyzer(workout_summary, activity_type="General"):
    """Uses Gemini 1.5 to analyze workout performance based on activity type."""

    # Define activity-specific guidance
    activity_specific_instructions = {
        "Run": "Analyze running pace, cadence, and endurance. Suggest interval training or long runs.",
        "Walk": "Assess walking speed and endurance. Suggest step count goals and posture improvement."
    }
    
    # Get specific instructions based on activity type
    activity_guidance = activity_specific_instructions.get(activity_type, "General fitness analysis.")

    prompt = f"""
    You are a fitness AI coach analyzing {activity_type} workout data.
    Based on this workout summary:
    {workout_summary}

    - {activity_guidance}
    - Identify strengths and weaknesses
    - Suggest improvements for endurance and speed
    - Highlight potential injury risks
    - Recommend a structured workout plan
    """
    
    model = genai.GenerativeModel("gemini-1.5-flash")
    response = model.generate_content(prompt)
    
    return response.text



def ai_training_planner(user_goal, activity_type="General"):
    """Creates a personalized training schedule using AI, based on the activity type."""
    
    # Define activity-specific guidance for training plans
    activity_specific_guidance = {
        "Run": "Focus on speed, endurance, and pacing strategies. Include interval runs, tempo runs, and long-distance runs.",
        "Walk": "Improve walking endurance and speed. Suggest step count goals and brisk walking strategies.",
    }
    
    # Get specific training plan guidance based on activity type
    training_guidance = activity_specific_guidance.get(activity_type, "General fitness training plan.")

    prompt = f"""
    You are an AI fitness coach designing a {activity_type} training plan.
    The user wants to achieve: {user_goal}
    
    - {training_guidance}
    - Provide a **4-week** structured training schedule.
    - Include recommended workout types (e.g., interval training, endurance sessions, strength training).
    - Define intensity levels and weekly progression strategies.
    - Suggest recovery and injury prevention techniques.
    """
    
    model = genai.GenerativeModel("gemini-1.5-flash")
    response = model.generate_content(prompt)
    
    return response.text




