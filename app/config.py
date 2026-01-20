import os
from dotenv import load_dotenv

load_dotenv()

# Database (default uses psycopg v3 driver)
DATABASE_URL = "postgresql+psycopg://postgres:dhvani%405225@localhost:5432/sleeper_bus_db"

# App settings
APP_NAME = "Sleeper Bus Ticket Booking System"
APP_VERSION = "1.0.0"
DEBUG = os.getenv("DEBUG", "False") == "True"

# JWT settings (if needed for future authentication)
SECRET_KEY = os.getenv("SECRET_KEY", "your-secret-key-change-in-production")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

# CORS settings
CORS_ORIGINS = [
    "http://localhost",
    "http://localhost:3000",
    "http://localhost:8000",
]