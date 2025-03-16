import pandas as pd
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.preprocessing import StandardScaler

def preprocess_data(df):
    """
    Prepares the data for similarity computation:
    - Converts time to minutes, distance to km
    - Computes pace (min/km)
    - Normalizes numeric features
    """
    df = df.copy()

    # Convert time to minutes and distance to km
    df["Elapsed Time (min)"] = df["Elapsed Time"]
    df["Distance (km)"] = df["Distance"] 
    df["Average Speed"] = df["Average Speed"]  # Convert m/s to km/h

    # Compute Pace (min/km), avoiding division by zero
    df["Pace (min/km)"] = np.where(df["Distance (km)"] > 0, df["Elapsed Time (min)"] / df["Distance (km)"], np.nan)

    # Convert Activity Date to datetime
    df["Activity Date"] = pd.to_datetime(df["Activity Date"])

    # Encode Activity Type (One-hot Encoding)
    df = pd.get_dummies(df, columns=["Activity Type"], prefix="Type")

    # Drop unnecessary columns
    df = df.drop(columns=["Activity ID", "Activity Name", "Activity Date", "Elapsed Time", "Distance"])

    # Handle NaN values
    df.fillna(df.mean(), inplace=True)

    return df

def content_based_recommender(df, selected_activity_type="All", top_n=5):
    """
    Recommends workouts similar to a user's past activities using content-based filtering.
    
    Parameters:
    - df: DataFrame containing workout data.
    - selected_activity_type: The type of activity to filter on (e.g., "Run", "Walk", "Ride").
    - top_n: Number of recommendations to generate.

    Returns:
    - DataFrame with recommended workouts.
    """
    feature_cols = ["Elapsed Time (min)", "Distance (km)", "Average Speed"]

    if df.empty:
        print("⚠️ WARNING: No workout data available.")
        return pd.DataFrame()

    # ✅ Step 1: Filter Data Based on Selected Activity Type
    if selected_activity_type != "All":
        df = df[df["Activity Type"] == selected_activity_type].copy()

    if df.empty:
        print(f"⚠️ WARNING: No {selected_activity_type} activities found for recommendation.")
        return pd.DataFrame()

    # ✅ Step 2: Preprocess Data
    df = preprocess_data(df)
    df.reset_index(drop=True, inplace=True)  # Reset index to match similarity matrix

    # ✅ Step 3: Standardize Features
    scaler = StandardScaler()
    df_features_scaled = scaler.fit_transform(df[feature_cols])

    # ✅ Step 4: Compute Cosine Similarity
    similarity_matrix = cosine_similarity(df_features_scaled)

    # ✅ Step 5: Select the most recent workout (last row in filtered df)
    latest_workout_idx = len(df) - 1  # Always the last index

    similarity_scores = list(enumerate(similarity_matrix[latest_workout_idx]))
    similarity_scores = sorted(similarity_scores, key=lambda x: x[1], reverse=True)

    recommended_indices = [idx for idx, _ in similarity_scores[1:top_n+1] if idx < len(df)]
    recommended_workouts = df.iloc[recommended_indices]

    print(f"🔍 DEBUG: Content-Based Recommendations Generated ({recommended_workouts.shape[0]} results) for {selected_activity_type}.")

    return recommended_workouts
