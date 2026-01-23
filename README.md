# 🚌 Sleeper Bus Ticket Booking System

A production-ready backend system for managing sleeper bus ticket bookings on the Ahmedabad-Mumbai route. Features real-time seat availability, dynamic pricing, ML-based booking confirmation predictions, and comprehensive booking management.

**Live API**: `http://localhost:8000/docs` (Swagger UI)  
**Tech Stack**: FastAPI + PostgreSQL + SQLAlchemy + ML (Logistic Regression)

---

## 📋 Project Overview

This system manages a **single sleeper bus** (40 seats) operating on the Ahmedabad-Mumbai route with 5 intermediate stations. It handles:

- ✅ Segment-based seat availability (prevents double-booking on overlapping routes)
- ✅ Dynamic pricing based on distance and seat type
- ✅ Multi-seat bookings with optional meal selection
- ✅ ML-powered booking confirmation probability prediction
- ✅ Flexible cancellation with tiered refund policy
- ✅ Booking history and management

---

## 📦 Part 1: Product & Quality Assurance

## ✨ Features

1. **Route & Station Selection** - Choose from 5 stations (Ahmedabad → Vadodara → Surat → Navsari → Mumbai) with intermediate boarding/alighting
2. **Real-time Seat Availability** - View available sleeper berths (Lower/Upper) with live status updates
3. **Smart Seat Booking** - Atomic multi-seat reservations with overlap detection to prevent double-booking
4. **Meal Selection** - Optional food ordering during checkout (Veg/Non-Veg/Beverages)
5. **Booking Confirmation** - Instant confirmation with unique booking reference and PNR
6. **Cancellation & Refunds** - Tiered refund policy (100%/50%/0% based on cancellation time)
7. **Booking History** - View all bookings by email with status tracking
8. **ML Prediction** - AI-powered confirmation probability scoring (50-95%) based on booking parameters

---

---

## 🚀 How to Run Locally

### Prerequisites
- Python 3.10+
- PostgreSQL 14+
- Git

### Setup Steps

```bash
# 1. Clone repository
git clone https://github.com/dhvanii5/Sleeper-Bus-Ticket-Booking-System
cd Sleeper-Bus-Ticket-Booking-System

# 2. Create virtual environment
python -m venv .venv
.venv\Scripts\activate  # Windows
source .venv/bin/activate  # Mac/Linux

# 3. Install dependencies
pip install -r requirements.txt

# 4. Configure database
# Edit app/config.py and update DATABASE_URL with your PostgreSQL credentials
# Format: postgresql+psycopg://user:password@localhost:5432/sleeper_bus_db

# 5. Initialize database
python scripts/init_db.py

# 6. Train ML model (optional but recommended)
python -m app.ml.train_model

# 7. Run server
uvicorn app.main:app --reload

# 8. Access API documentation
# Open browser: http://localhost:8000/docs
```

### Environment Variables (Optional)
Create a `.env` file in the project root:
```env
DATABASE_URL=postgresql+psycopg://user:password@localhost:5432/sleeper_bus_db
DEBUG_MODE=True
```

### Running Tests
```bash
# Basic smoke tests
python tests/test_basic.py

# Comprehensive endpoint tests
python tests/test_comprehensive.py

# Run with pytest
pytest tests/ -v
```

---

## 📁 Project Structure

```
Sleeper-Bus-Ticket-Booking-System/
├── app/
│   ├── main.py                    # FastAPI application entry
│   ├── config.py                  # Configuration settings
│   ├── database.py                # Database connection
│   ├── api/v1/                    # API endpoints (versioned)
│   │   ├── bookings.py
│   │   ├── seats.py
│   │   ├── stations.py
│   │   ├── meals.py
│   │   └── predictions.py
│   ├── models/                    # SQLAlchemy ORM models
│   │   ├── booking.py
│   │   ├── seat.py
│   │   ├── station.py
│   │   └── meal.py
│   ├── schemas/                   # Pydantic validation schemas
│   │   └── schemas.py
│   ├── services/                  # Business logic layer
│   │   ├── booking_service.py
│   │   ├── seat_service.py
│   │   ├── station_service.py
│   │   ├── meal_service.py
│   │   └── prediction_service.py
│   ├── ml/                        # Machine Learning system
│   │   ├── train_model.py         # Model training script
│   │   ├── predictor.py           # Inference logic
│   │   └── saved_models/          # Trained models
│   ├── core/                      # Core utilities
│   │   └── common.py              # Exceptions & utilities
│   └── utils/                     # Helper functions
│       └── utils.py
├── scripts/
│   ├── init_db.py                 # Database initialization
│   └── generate_mock_data.py     # Test data generator
├── tests/                         # Test suite
│   ├── test_basic.py
│   ├── test_comprehensive.py
│   └── conftest.py
├── docs/                          # Documentation
│   └── PROJECT_STRUCTURE.md
├── PREDICTION_APPROACH.md         # ML methodology (root-level)
├── requirements.txt               # Python dependencies
└── README.md                      # This file
```

---

## 🏗️ Architecture

**Layered Architecture**:
- **API Layer** (`api/v1/`) - HTTP endpoints, request/response handling
- **Service Layer** (`services/`) - Business logic, validations
- **Data Layer** (`models/`) - Database schema, ORM models
- **Schema Layer** (`schemas/`) - Data validation and serialization

**Design Principles**:
- ✅ Single Responsibility Principle
- ✅ Dependency Injection (FastAPI's `Depends`)
- ✅ Separation of Concerns
- ✅ RESTful API design
- ✅ Clean Code with meaningful comments

---

## 📊 Database Schema

**Tables**:
- `stations` - Route stations with timings
- `seats` - Seat inventory (40 sleeper berths)
- `seat_availability` - Booking records for route segments
- `bookings` - Customer reservations
- `booking_meals` - Meal selections (many-to-many)
- `meals` - Food menu items

**Key Relationships**:
- Booking → Stations (Many-to-One for origin/destination)
- Booking → Seats (Many-to-Many via SeatAvailability)
- Booking → Meals (Many-to-Many via BookingMeal)

---

## 🎯 Key Highlights

1. **Segment-Based Availability** - Prevents double-booking on overlapping routes (e.g., seat booked for Ahmedabad-Surat can't be booked for Vadodara-Mumbai)
2. **Dynamic Pricing** - Base Price × Distance Multiplier × Seat Type Multiplier
3. **ML Integration** - Production-ready Logistic Regression model with coefficient-based explanations
4. **Atomic Transactions** - All-or-nothing booking (prevents partial reservations)
5. **Comprehensive Validation** - Pydantic schemas enforce data integrity
6. **Clean Architecture** - Modular, testable, and maintainable codebase

---

## 📝 License

MIT License - Feel free to use for learning and projects

---

## 👤 Author

**Your Name**  
GitHub: [@dhvanii5](https://github.com/dhvanii5)  
Email: dhvanikapatel05@gmail.com

---

## 🙏 Acknowledgments

- FastAPI documentation and community
- SQLAlchemy ORM patterns
- Scikit-learn for ML implementation

---

**⭐ Star this repo if you found it helpful!**

---

## 🛠️ Tech Stack

| Layer | Technology | Purpose |
|-------|-----------|---------|
| **API Framework** | FastAPI 0.109 | High-performance async REST API |
| **Database** | PostgreSQL + psycopg3 | Relational data storage with modern driver |
| **ORM** | SQLAlchemy 2.0 | Database modeling and queries |
| **Validation** | Pydantic 2.5 | Request/response schema validation |
| **ML Model** | Scikit-learn 1.3 | Logistic Regression for predictions |
| **Data Processing** | Pandas + NumPy | Dataset handling and feature engineering |
| **Server** | Uvicorn | ASGI server with auto-reload |
| **Testing** | Pytest + httpx | Unit and integration testing |

---

## 🌐 API Endpoints

### Stations
| Method | Endpoint | Description |
|--------|----------|-------------|
| `GET` | `/api/v1/stations` | List all route stations with timings |

### Seats
| Method | Endpoint | Description |
|--------|----------|-------------|
| `GET` | `/api/v1/seats` | Get available seats for route & date (with pricing) |
| `GET` | `/api/v1/seats/{seat_id}` | Get specific seat details & availability |

### Bookings
| Method | Endpoint | Description |
|--------|----------|-------------|
| `POST` | `/api/v1/bookings` | Create new booking (returns confirmation + PNR) |
| `GET` | `/api/v1/bookings/{booking_ref}` | Get booking details by reference |
| `GET` | `/api/v1/bookings/history/{email}` | View all bookings for an email |
| `DELETE` | `/api/v1/bookings/{booking_ref}` | Cancel booking (with refund calculation) |
| `PUT` | `/api/v1/bookings/{booking_ref}/meals` | Update meal selection |

### Meals
| Method | Endpoint | Description |
|--------|----------|-------------|
| `GET` | `/api/v1/meals` | List available meal options |

### Predictions (ML)
| Method | Endpoint | Description |
|--------|----------|-------------|
| `POST` | `/prediction/booking-confirmation` | Get booking confirmation probability |

**Full API Documentation**: Visit `/docs` after starting the server

---

---

## Test Cases

### 1. Functional Test Cases
- **User can view available seats** - GET `/api/v1/seats` returns list with pricing
- **User cannot book already booked seat** - Returns HTTP 409 Conflict error
- **Meal selection saved correctly** - Booking response includes selected meals
- **Cancelled seat becomes available** - Seat shows as available after cancellation
- **Booking probability API returns percentage** - Prediction endpoint returns 50-95% score
- **Multi-seat booking is atomic** - All seats reserved or none
- **Dynamic pricing works** - Price varies by distance and seat type
- **Refund policy applied correctly** - Refund % based on cancellation timeline
- **PNR and booking reference generated** - Unique identifiers created
- **Email validation enforced** - Invalid emails rejected with 422 error

### 2. Edge Cases
- **Booking last available seat** - Seat properly blocked, next request gets 409
- **Cancelling already cancelled booking** - Returns 400 Bad Request
- **Invalid seat number** - Returns 400 with clear error message
- **Backwards route booking** - Detects and rejects Mumbai → Ahmedabad
- **Past travel date** - Validation rejects dates before today
- **Overlapping route segments** - Prevents seat booking if any segment conflicts
- **Missing required parameters** - Returns 422 with validation details
- **Booking with 0 seats** - Rejected by min_items=1 validation
- **More than 5 seats requested** - Rejected by max_items=5 validation
- **Phone number not 10 digits** - Pattern validation rejects invalid format

### 3. UI/UX Validation (API Response Quality)
- **Seat status clearly indicated** - Response shows "available" vs "booked"
- **Error messages are human-readable** - No raw stack traces in API responses
- **Booking confirmation includes all details** - Complete journey info in response
- **Proper HTTP status codes** - 200 (OK), 400 (Bad Request), 404 (Not Found), 409 (Conflict), 422 (Validation Error)
- **Consistent data formats** - Dates in YYYY-MM-DD, times in HH:MM
- **ML factor breakdown provided** - Prediction response shows contributing factors
- **Cancellation response shows refund details** - Amount, percentage, status clearly stated

---

## 🎨 UI/UX Prototype


**Figma Link**: (https://www.figma.com/proto/ZstZR2fiWkkzEygI28BkjY/sleeper-bus-booking-system?node-id=10-649&t=AyrodbZUA0mMalPv-1)

---

## 🤖 Prediction Feature Summary

**What**: AI-powered booking confirmation probability  
**How**: Logistic Regression model trained on synthetic historical data  
**Input Features**: Lead time, occupancy, seat type, route type, holiday season, party size  
**Output**: Confirmation probability (50-95%), Cancellation risk (8-25%), Recommendation (HIGH_CHANCE/GOOD_CHANCE/REVIEW_SUGGESTED/MONITOR_CLOSELY)  

**Explainability**: Factor-based impact descriptions (e.g., "Lead time: Moderate positive impact")  

**Details**: See [PREDICTION_APPROACH.md](PREDICTION_APPROACH.md) for complete methodology


**Author**: Dhvani  
**Version**: 1.1.0 (Refactored)
