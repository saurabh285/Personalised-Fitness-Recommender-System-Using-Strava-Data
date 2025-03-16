import os
import subprocess
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Step 1️⃣: Start Flask Backend (Authentication API)
flask_command = "python src/auth.py"  # ✅ Updated to reflect src folder
print("🚀 Starting Flask Backend for Authentication...")
flask_process = subprocess.Popen(flask_command, shell=True)

# Step 2️⃣: Start Streamlit UI
streamlit_command = "streamlit run src/ui.py --server.port 8501 --server.address 0.0.0.0"
print("🚀 Starting Streamlit UI on port 8501...")
subprocess.run(streamlit_command, shell=True)

# Step 3️⃣: Keep the Flask API running
flask_process.wait()
