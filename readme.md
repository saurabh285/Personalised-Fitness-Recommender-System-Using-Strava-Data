# AI-Powered Fitness Recommender & Performance Predictor

## Overview
The **AI-Powered Fitness Recommender & Performance Predictor** is a web-based application that integrates **Strava API** and **AI-powered analysis** to provide personalized workout recommendations, training plans, and performance predictions. Users can fetch workout data from Strava or upload a CSV file to analyze their fitness activities.

## Features
- **Strava API Integration**: Fetch workout data from your Strava account.
- **CSV Upload Support**: Upload fitness activity data manually.
- **AI Workout Analysis**: Identify strengths, weaknesses, and areas for improvement.
- **AI Training Plan Generator**: Get a structured 4-week training plan based on your goals.
- **AI Performance Predictor**: Forecast your future race times and fitness progress.
- **Personalized Recommendations**: Get **content-based filtering (CBF)** recommendations based on past activities.
- **Activity Type Selection**: Filter analysis based on **Run, Walk, Workout, WeightTraining, Swim, Ride, or All**.

---

##  Installation & Setup
### Prerequisites
Ensure you have the following installed:
- **Python 3.10**
- **Pip & Virtual Environment**

### Step 1: Clone the Repository
```bash
git clone https://github.com/yourusername/fitness-recommender.git
cd fitness-recommender
```

### Step 2: Create a Virtual Environment
```bash
python -m venv venv
source venv/bin/activate  # On macOS/Linux
venv\Scripts\activate    # On Windows
```

### Step 3: Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 4: Set Up Environment Variables
Create a `.env` file in the project root and add your credentials:
```
STRAVA_CLIENT_ID=your_client_id
STRAVA_CLIENT_SECRET=your_client_secret
FLASK_SECRET_KEY=your_flask_secret
GEMINI_API_KEY=your_google_gemini_api_key
```

### Step 5: Run the Application
Start the **Flask backend** and **Streamlit UI** using:
```bash
python main.py
```
This will:
1. Start the **Flask Authentication API** on port **5001**.
2. Launch the **Streamlit UI** on port **8501**.

---

##  Usage
### 1️⃣ Import Workout Data
- **Strava API**: Log in via Strava to fetch workout data.
- **CSV Upload**: Manually upload a CSV file.

### 2️⃣ Choose Activity Type
- Select from **Run, Walk, Workout, WeightTraining, Swim, Ride, or All**.

### 3️⃣ AI-Powered Analysis & Recommendations
- **Workout Analysis**: AI evaluates your performance and suggests improvements.
- **Training Plan**: AI generates a 4-week customized training schedule.
- **Performance Predictor**: Predicts future fitness improvements based on your history.
- **Workout Recommendations**: Suggests similar activities using **Content-Based Filtering (CBF)**.

---

## Folder Structure
```
fitness-recommender/
│── src/
│   │── auth.py                # Strava OAuth Authentication (Flask API)
│   │── ui.py                  # Streamlit UI for the application
│   │── data_loader.py         # Data fetching & preprocessing from Strava
│   │── recommender_system.py  # AI-powered recommendations (CBF)
│   │── agents.py              # AI workout analysis & training planner
│── main.py                    # Starts Flask & Streamlit services
│── requirements.txt            # Python dependencies
│── .env                        # Environment variables (hidden)
│── README.md                   # Documentation
```
⭐ **If you like this project, please consider giving it a star on GitHub!** ⭐

