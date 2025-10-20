# import os

# # TEMP_DIR = os.path.join(os.path.dirname(__file__), "..", "temp_data")
# # os.makedirs(TEMP_DIR, exist_ok=True)
# APP_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))  # this will always point to app/
# TEMP_DIR = os.path.join(APP_ROOT, "temp_data")
# os.makedirs(TEMP_DIR, exist_ok=True)
# import os

# # Get the absolute path to the app/ directory
# APP_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))  # one level up from utils/

# # Create temp_data folder inside app/
# TEMP_DIR = os.path.join(APP_ROOT, "temp_data")

# # Ensure folder exists
# os.makedirs(TEMP_DIR, exist_ok=True)
import os

# Get absolute path of the current file
CURRENT_FILE = os.path.abspath(__file__)

# Go two levels up from utils → app → adf-backend
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(CURRENT_FILE)))

# Now go into app/
APP_ROOT = os.path.join(PROJECT_ROOT, "app")

# Ensure temp_data exists inside app/
TEMP_DIR = os.path.join(APP_ROOT, "temp_data")
os.makedirs(TEMP_DIR, exist_ok=True)

print(f"[INFO] TEMP_DIR set to: {TEMP_DIR}")
