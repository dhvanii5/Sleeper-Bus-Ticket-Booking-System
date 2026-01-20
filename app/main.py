from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .api.v1 import stations, seats, bookings, meals, predictions

app = FastAPI(
    title="Sleeper Bus Ticket Booking System",
    description="API for booking sleeper bus tickets",
    version="1.0.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(stations.router, prefix="/api/v1/stations", tags=["Stations"])
app.include_router(seats.router, prefix="/api/v1/seats", tags=["Seats"])
app.include_router(bookings.router, prefix="/api/v1/bookings", tags=["Bookings"])
app.include_router(meals.router, prefix="/api/v1/meals", tags=["Meals"])
app.include_router(predictions.router, prefix="/api/v1/predictions", tags=["Predictions"])

@app.get("/")
async def read_root():
    return {"message": "Welcome to the Sleeper Bus Ticket Booking System"}