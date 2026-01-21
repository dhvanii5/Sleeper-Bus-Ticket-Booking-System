"""
Configuration Module for Sleeper Bus Ticket Booking System

This module contains all application-wide configuration settings including:
- Database connection parameters
- Application metadata
- Security settings
- CORS configuration
- Business domain configuration (Bus & Route details)

All configuration values can be overridden using environment variables
for different deployment environments (dev/staging/prod).
"""

import os
from dotenv import load_dotenv

# Load environment variables from .env file (if present)
load_dotenv()

# =============================================================================
# DATABASE CONFIGURATION
# =============================================================================
# PostgreSQL database connection string using psycopg3 driver
# Format: postgresql+psycopg://user:password@host:port/database
# psycopg3 is faster and more modern than psycopg2
DATABASE_URL = "postgresql+psycopg://postgres:dhvani%405225@localhost:5432/sleeper_bus_db"

# =============================================================================
# APPLICATION SETTINGS
# =============================================================================
APP_NAME = "Sleeper Bus Ticket Booking System"
APP_VERSION = "1.0.0"
DEBUG = os.getenv("DEBUG", "False") == "True"  # Enable debug mode via env var

# =============================================================================
# SECURITY SETTINGS
# =============================================================================
# JWT (JSON Web Token) settings for future authentication/authorization
# These are currently not used but prepared for future enhancement
SECRET_KEY = os.getenv("SECRET_KEY", "your-secret-key-change-in-production")
ALGORITHM = "HS256"  # HMAC with SHA-256 for JWT signing
ACCESS_TOKEN_EXPIRE_MINUTES = 30  # Token validity duration

# =============================================================================
# CORS (Cross-Origin Resource Sharing) CONFIGURATION
# =============================================================================
# Allowed origins for cross-origin requests (for frontend apps)
CORS_ORIGINS = [
    "http://localhost",       # Local development
    "http://localhost:3000",  # React default port
    "http://localhost:8000",  # FastAPI default port
]

# =============================================================================
# BUSINESS DOMAIN CONFIGURATION
# =============================================================================

# Bus Configuration - Single Bus System
# This system is designed to manage exactly ONE bus with 40 sleeper seats
BUS_CONFIG = {
    "bus_id": "BUS001",           # Unique identifier for the bus
    "total_seats": 40,            # Total capacity
    "seat_layout": {
        "lower_berth": 20,        # Lower berth seats: S01-S20 (more expensive)
        "upper_berth": 20         # Upper berth seats: S21-S40 (less expensive)
    },
    "route": "Ahmedabad -> Mumbai"  # Fixed route
}

# Stations Configuration - Fixed Route with 5 Stops
# Each station has:
# - name: Display name
# - sequence: Order in route (1-5, used for segment validation)
# - arrival_time: When bus arrives at this station
# - departure_time: When bus departs from this station
# - distance_km: Distance from origin (used for dynamic pricing)
STATIONS = [
    {
        "name": "Ahmedabad",
        "sequence": 1,
        "arrival_time": "20:00",     # Journey starts here
        "departure_time": "20:15",   # 15 min buffer for boarding
        "distance_km": 0              # Origin point
    },
    {
        "name": "Vadodara",
        "sequence": 2,
        "arrival_time": "22:00",     # ~2 hours from Ahmedabad
        "departure_time": "22:15",
        "distance_km": 100
    },
    {
        "name": "Surat",
        "sequence": 3,
        "arrival_time": "00:30",     # Night arrival
        "departure_time": "00:45",
        "distance_km": 250
    },
    {
        "name": "Vapi",
        "sequence": 4,
        "arrival_time": "02:00",
        "departure_time": "02:15",
        "distance_km": 350
    },
    {
        "name": "Mumbai",
        "sequence": 5,
        "arrival_time": "05:00",     # Final destination (early morning)
        "departure_time": "05:00",   # No departure (end of route)
        "distance_km": 500
    }
]