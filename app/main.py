"""
Main Application Entry Point - Sleeper Bus Ticket Booking System

This module initializes the FastAPI application and configures:
- CORS middleware for cross-origin requests
- API routing for all endpoints (v1)
- Application metadata (title, description, version)

The application follows a layered architecture:
    API Layer (this file) → Service Layer → Data Layer (Models)

To run the application:
    uvicorn app.main:app --reload
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .api.v1 import stations, seats, bookings, meals, predictions
from .routes import prediction_routes

# =============================================================================
# FASTAPI APPLICATION INITIALIZATION
# =============================================================================
app = FastAPI(
    title="Sleeper Bus Ticket Booking System",
    description="RESTful API for managing ticket bookings on the Ahmedabad-Mumbai sleeper bus route",
    version="1.0.0",
    docs_url="/docs",      # Swagger UI at /docs
    redoc_url="/redoc"     # ReDoc documentation at /redoc
)

# =============================================================================
# MIDDLEWARE CONFIGURATION
# =============================================================================
# CORS (Cross-Origin Resource Sharing) - Allows frontend apps to access API
# Currently permissive (*) for development; restrict in production
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],         # TODO: Restrict to specific domains in prod
    allow_credentials=True,       # Allow cookies/auth headers
    allow_methods=["*"],          # Allow all HTTP methods (GET, POST, etc.)
    allow_headers=["*"],          # Allow all request headers
)

# =============================================================================
# API ROUTE REGISTRATION (Version 1)
# =============================================================================
# All routes are versioned under /api/v1 for future compatibility

# Stations - Route and timing information
# GET /api/v1/stations - List all stations with schedule
app.include_router(stations.router, prefix="/api/v1", tags=["Stations"])

# Seats - Availability and pricing
# GET /api/v1/seats - Check seat availability for date/route
app.include_router(seats.router, prefix="/api/v1/seats", tags=["Seats"])

# Bookings - Core ticket booking operations
# POST /api/v1/bookings - Create new booking
# GET /api/v1/bookings/{ref} - Get booking details
# DELETE /api/v1/bookings/{ref} - Cancel booking
app.include_router(bookings.router, prefix="/api/v1/bookings", tags=["Bookings"])

# Meals - Food catalog
# GET /api/v1/meals - List available meals
app.include_router(meals.router, prefix="/api/v1/meals", tags=["Meals"])

# Predictions - AI/ML features
# POST /api/v1/predictions/predict - Get booking confirmation probability
app.include_router(predictions.router, prefix="/api/v1/predictions", tags=["Predictions"])

# New Prediction API (from additional task requirements)
app.include_router(prediction_routes.router, prefix="/api/prediction", tags=["Prediction ML"])

# =============================================================================
# ROOT ENDPOINT
# =============================================================================
@app.get("/", tags=["Root"])
async def read_root():
    """
    Root endpoint providing API welcome message and basic info.
    
    Returns:
        dict: Welcome message with API status
    """
    return {
        "message": "Welcome to the Sleeper Bus Ticket Booking System",
        "version": "1.0.0",
        "docs": "/docs",      # Link to Swagger UI
        "status": "active"
    }