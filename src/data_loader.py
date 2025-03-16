import pandas as pd
import requests
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Strava API Credentials
CLIENT_ID = os.getenv("STRAVA_CLIENT_ID")
CLIENT_SECRET = os.getenv("STRAVA_CLIENT_SECRET")
TOKEN_URL = "https://www.strava.com/oauth/token"
ACTIVITIES_URL = "https://www.strava.com/api/v3/athlete/activities"

def get_strava_access_token(refresh_token: str) -> str:
    """Fetches a new Strava access token using the refresh token."""
    response = requests.post(
        TOKEN_URL,
        data={
            "client_id": CLIENT_ID,
            "client_secret": CLIENT_SECRET,
            "grant_type": "refresh_token",
            "refresh_token": refresh_token
        }
    )
    response_data = response.json()
    
    if "access_token" not in response_data:
        print("❌ ERROR: Failed to get access token:", response_data)
        return None
    
    print("✅ [DEBUG] New Access Token:", response_data["access_token"])
    return response_data["access_token"]

def fetch_strava_activities(refresh_token, per_page=200):
    """Fetches and processes all workout data from Strava API using pagination."""
    
    # Get new access token
    access_token = get_strava_access_token(refresh_token)
    if not access_token:
        return pd.DataFrame()

    headers = {"Authorization": f"Bearer {access_token}"}
    all_activities = []
    page = 1

    while True:
        response = requests.get(
            ACTIVITIES_URL, 
            headers=headers,
            params={"per_page": per_page, "page": page}  # Request multiple pages
        )
        raw_data = response.json()

        if not isinstance(raw_data, list) or len(raw_data) == 0:
            break  # Stop when no more activities are returned

        all_activities.extend(raw_data)
        page += 1  # Move to the next page

        print(f"✅ Fetched {len(raw_data)} activities from page {page}")  # Debugging

    # Convert to DataFrame
    df = pd.DataFrame(all_activities)

    if df.empty:
        print("❌ ERROR: No activities found in API response.")
        return pd.DataFrame()

    # Keep only required columns
    required_columns = {
        "id": "Activity ID",
        "start_date": "Activity Date",
        "name": "Activity Name",
        "type": "Activity Type",
        "elapsed_time": "Elapsed Time",
        "distance": "Distance",
        # "max_speed": "Max Speed",
        "average_speed": "Average Speed",
        "total_elevation_gain": "Elevation Gain"
    }

    df = df[list(required_columns.keys())].rename(columns=required_columns)
    df = df[df["Activity Type"].isin(["Run", "Walk"])]

    if df.empty:
        print("⚠️ WARNING: No 'Run' or 'Walk' activities found in the data!")
        return pd.DataFrame()

    # Convert types
    df["Activity Date"] = pd.to_datetime(df["Activity Date"], errors="coerce")
    df["Elapsed Time"] = df["Elapsed Time"] / 60  # Convert to minutes
    df["Distance"] = df["Distance"] / 1000  # Convert to kilometers
    # df["Max Speed"] = df["Max Speed"] * 3.6
    df["Average Speed"] = df["Average Speed"] * 3.6
    # Fill missing values
    df.fillna(0, inplace=True)

    print(f"✅ SUCCESS: {len(df)} activities fetched.")  # Debugging output

    return df
