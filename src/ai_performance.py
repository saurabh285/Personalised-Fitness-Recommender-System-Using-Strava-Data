import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error
import numpy as np

def prepare_data(df):
    """Transforms workout data for machine learning prediction."""
    df = df.copy()
    
    # Convert time to minutes and distance to km
    df['Elapsed Time (min)'] = df['Elapsed Time'] / 60
    df['Distance (km)'] = df['Distance'] / 1000

    # 🛠 Fix division by zero issue
    df['Pace (min/km)'] = np.where(df['Distance (km)'] > 0, df['Elapsed Time (min)'] / df['Distance (km)'], np.nan)
    
    # Convert Activity Date
    df['Activity Date'] = pd.to_datetime(df['Activity Date'], errors='coerce')
    df['Day of Week'] = df['Activity Date'].dt.dayofweek  # Monday=0, Sunday=6
    df['Time of Day'] = df['Activity Date'].dt.hour
    
    # One-hot encoding for activity types (Run, Walk)
    df = pd.get_dummies(df, columns=['Activity Type'], prefix='Type')

    # Handle missing and infinite values
    df.replace([np.inf, -np.inf], np.nan, inplace=True)
    df.dropna(inplace=True)  # Drop rows with NaN or infinite values

    # Filter out unrealistic pace values (>20 min/km or <2 min/km)
    df = df[(df['Pace (min/km)'] > 2) & (df['Pace (min/km)'] < 20)]
    
    # Drop unnecessary columns
    df = df.drop(columns=['Activity ID', 'Activity Name', 'Activity Date', 'Elapsed Time', 'Distance'], errors='ignore')

    return df

def train_model(df):
    """Trains a regression model to predict pace."""
    if df.empty:
        raise ValueError("❌ Not enough valid data to train the model.")

    try:
        X = df[['Type_Run', 'Type_Walk', 'Distance (km)', 'Day of Week', 'Time of Day', 'Max Speed', 'Average Speed']]
        y = df['Pace (min/km)']

        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

        model = LinearRegression()
        model.fit(X_train, y_train)

        y_pred = model.predict(X_test)
        rmse = mean_squared_error(y_test, y_pred, squared=False)

        print(f"✅ Model Trained. RMSE: {rmse:.2f} min/km")

        return model

    except Exception as e:
        print(f"❌ ERROR: Model training failed - {e}")
        return None

def predict_5k_time(model):
    """Predicts the expected time for a 5K run."""
    new_data = pd.DataFrame({'Type_Run': [1], 'Type_Walk': [0], 'Distance (km)': [5], 
                             'Day of Week': [3], 'Time of Day': [10], 'Max Speed':[3.5], 
                             'Average Speed':[2.5]})  # Example values

    try:
        predicted_pace_5k = model.predict(new_data)[0]
        predicted_time_5k = predicted_pace_5k * 5
        return predicted_time_5k

    except Exception as e:
        print(f"❌ ERROR: Prediction failed - {e}")
        return None

def ai_performance_predictor(df):
    """Generates an AI-based prediction of future race times."""
    
    if df.empty or df.shape[0] < 5:  # Need at least 5 workouts for training
        return "⚠️ Not enough workout data to predict future performance."

    df_prepared = prepare_data(df)

    print("🔍 DEBUG: Data After Processing")
    print(df_prepared.head())  # Show first few rows of processed data
    print(f"🔍 DEBUG: Data Shape -> {df_prepared.shape}")

    if df_prepared.empty or 'Pace (min/km)' not in df_prepared.columns:
        return "⚠️ Insufficient valid data for prediction."

    model = train_model(df_prepared)

    if model is None:
        return "⚠️ Failed to train the model due to insufficient data."

    predicted_time_5k = predict_5k_time(model)

    if predicted_time_5k is None:
        return "⚠️ Unable to predict 5K race time."

    return f"📈 Based on your training data, your predicted 5K race time is **{predicted_time_5k:.2f} minutes**."
