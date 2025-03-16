from flask import Flask, request, redirect, session
import requests
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

CLIENT_ID = os.getenv("STRAVA_CLIENT_ID")
CLIENT_SECRET = os.getenv("STRAVA_CLIENT_SECRET")
REDIRECT_URI = "http://127.0.0.1:5001/callback"
TOKEN_URL = "https://www.strava.com/oauth/token"

app = Flask(__name__)
app.secret_key = os.getenv("FLASK_SECRET_KEY")

@app.route("/")
def index():
    return redirect("/login")

@app.route("/login")
def login():
    """Redirects user to Strava login for authentication."""
    auth_url = f"https://www.strava.com/oauth/authorize?client_id={CLIENT_ID}&response_type=code&redirect_uri={REDIRECT_URI}&approval_prompt=force&scope=read,activity:read_all"
    return redirect(auth_url)

@app.route("/callback")
def callback():
    """Handles Strava callback and retrieves refresh token."""
    auth_code = request.args.get("code")

    if not auth_code:
        return "❌ Authorization failed! No code received.", 400

    # Exchange authorization code for refresh token
    response = requests.post(
        TOKEN_URL,
        data={
            "client_id": CLIENT_ID,
            "client_secret": CLIENT_SECRET,
            "code": auth_code,
            "grant_type": "authorization_code"
        }
    )

    response_data = response.json()
    
    if "refresh_token" not in response_data:
        return f"❌ Error fetching refresh token: {response_data}", 400

    refresh_token = response_data["refresh_token"]
    access_token = response_data["access_token"]
    
    print(f"✅ [DEBUG] New Refresh Token: {refresh_token}")
    print(f"✅ [DEBUG] New Access Token: {access_token}")

    # Redirect to Streamlit UI with refresh token
    return redirect(f"http://localhost:8501?refresh_token={refresh_token}")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5001, debug=True)
