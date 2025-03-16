from src.data_loader import fetch_strava_activities

# Ask user for their refresh token
user_refresh_token = input("Enter your Strava refresh token: ")

# Fetch and display activities
activities = fetch_strava_activities(user_refresh_token)

if activities:
    print("Fetched User Activities:", activities[:3])  # Show first 3 activities
else:
    print("Failed to fetch activities!")
