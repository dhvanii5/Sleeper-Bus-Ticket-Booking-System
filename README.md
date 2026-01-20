# Sleeper Bus Ticket Booking System

A FastAPI-based backend system for managing sleeper bus ticket bookings with dynamic pricing, real-time seat availability, and meal management.

## Features

- **Seat Management**: Real-time seat availability tracking with route-based segment booking
- **Dynamic Pricing**: Distance-based and seat-type based pricing multipliers
- **Booking System**: Complete booking lifecycle with cancellation and refund policies
- **Meal Management**: Multiple meal selection with customization per passenger
- **Route Optimization**: Station-based route management with sequence tracking
- **Booking Predictions**: ML-based booking confirmation probability predictions
- **Comprehensive Validation**: Email, phone, station combination, and booking validation
- **Error Handling**: Custom exceptions for all business logic failures

## Project Structure

```
sleeper-bus-booking/
├── app/
│   ├── __init__.py
│   ├── main.py                 # FastAPI app initialization
│   ├── config.py               # Configuration settings
│   ├── database.py             # Database connection setup
│   │
│   ├── models/                 # SQLAlchemy ORM models
│   │   ├── __init__.py
│   │   ├── user.py
│   │   ├── seat.py
│   │   ├── booking.py
│   │   ├── meal.py
│   │   └── station.py
│   │
│   ├── schemas/                # Pydantic schemas (request/response)
│   │   ├── __init__.py
│   │   └── seat.py
│   │
│   ├── api/                    # API routes
│   │   ├── __init__.py
│   │   ├── dependencies.py     # Shared dependencies
│   │   └── v1/
│   │       ├── __init__.py
│   │       ├── seats.py
│   │       ├── bookings.py
│   │       ├── meals.py
│   │       ├── stations.py
│   │       └── predictions.py
│   │
│   ├── services/               # Business logic layer
│   │   ├── __init__.py
│   │   ├── seat_service.py
│   │   ├── booking_service.py
│   │   ├── meal_service.py
│   │   ├── station_service.py
│   │   └── prediction_service.py
│   │
│   ├── utils/                  # Utility functions
│   │   ├── __init__.py
│   │   ├── validators.py
│   │   └── helpers.py
│   │
│   └── core/                   # Core configurations
│       ├── __init__.py
│       ├── security.py
│       └── exceptions.py
│
├── tests/                      # Test cases
│   ├── __init__.py
│   ├── conftest.py
│   ├── test_seats.py
│   ├── test_bookings.py
│   └── test_meals.py
│
├── requirements.txt
├── .env.example
├── .gitignore
└── README.md

## Technologies

- **FastAPI** 0.109.0 - Modern, fast web framework
- **Uvicorn** 0.27.0 - ASGI server
- **SQLAlchemy** 2.0.25 - ORM for database operations
- **Pydantic** 2.5.3 - Data validation
- **PostgreSQL** - Production database
- **Pytest** 7.4.4 - Testing framework

## Setup Instructions

### 1. Create Virtual Environment

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### 3. Setup Environment Variables

```bash
cp .env.example .env
# Edit .env with your database credentials
```

### 4. Database Setup

```bash
# Create PostgreSQL database
createdb sleeper_bus_db

# Run migrations (if using Alembic)
alembic upgrade head
```

### 5. Run the Application

```bash
uvicorn app.main:app --reload
```

The API will be available at `http://localhost:8000`

### API Documentation

- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

## API Endpoints

### Stations
- `GET /api/v1/stations/` - List all stations
- `GET /api/v1/stations/{station_id}` - Get station details
- `POST /api/v1/stations/` - Create new station

### Seats
- `GET /api/v1/seats/availability` - Get available seats for route/date
- `GET /api/v1/seats/{seat_id}` - Get seat details

### Bookings
- `POST /api/v1/bookings/` - Create booking
- `GET /api/v1/bookings/{booking_reference}` - Get booking details
- `GET /api/v1/bookings/history/{email}` - Get booking history
- `DELETE /api/v1/bookings/{booking_reference}` - Cancel booking
- `PUT /api/v1/bookings/{booking_reference}/meals` - Update meals

### Meals
- `GET /api/v1/meals/` - List available meals
- `GET /api/v1/meals/category/{category}` - Get meals by category
- `GET /api/v1/meals/{meal_id}` - Get meal details
- `POST /api/v1/meals/` - Create new meal
- `PUT /api/v1/meals/{meal_id}/availability/{is_available}` - Update availability

### Predictions
- `POST /api/v1/predictions/booking-confirmation` - Get booking confirmation probability

## Business Logic Features

### Dynamic Pricing
- **Distance Multiplier**: 0-100km (1.0x), 100-300km (1.2x), 300km+ (1.5x)
- **Seat Type Multiplier**: Upper berth (1.0x), Lower berth (1.3x)
- **Formula**: Base Price × Distance Multiplier × Seat Type Multiplier

### Cancellation Policy
- **24+ hours before**: 100% refund
- **12-24 hours before**: 50% refund
- **Less than 12 hours**: No refund

### Seat Availability
- Route-based segment tracking
- Overlapping booking detection
- Multi-segment route support

### Booking Reference Format
`BUS-FROM-TO-YYYYMMDD-RANDOM`
Example: `BUS-AHM-MUM-20250125-A1B2`

## Error Handling

Custom exceptions for:
- `SeatNotAvailableException` - Seat unavailable for route
- `BookingNotFoundException` - Booking not found
- `InvalidStationException` - Invalid station combination
- `CancellationNotAllowedException` - Cancellation restrictions
- `DoubleBookingException` - Seat already booked
- `InvalidBookingException` - Invalid booking details

## Testing

```bash
# Run all tests
pytest

# Run with verbose output
pytest -v

# Run specific test file
pytest tests/test_bookings.py
```

## Future Enhancements

- User authentication and authorization
- Payment gateway integration
- Email notifications
- SMS notifications
- Admin dashboard
- Advanced ML predictions
- Real-time WebSocket updates
- Multi-language support

## Contributing

1. Create a feature branch
2. Make your changes
3. Write tests
4. Submit a pull request

## License

MIT
