# Sleeper Bus Ticket Booking System

A comprehensive backend system for managing bookings for a single sleeper bus operating on the Ahmedabad-Mumbai route. Built with FastAPI, SQLAlchemy, and PostgreSQL.

## 🏗️ Project Structure

```
Sleeper-Bus-Ticket-Booking-System/
│
├── app/                          # Main application package
│   ├── main.py                   # FastAPI application entry point
│   ├── config.py                 # Configuration settings
│   ├── database.py               # Database connection setup
│   │
│   ├── api/                      # API layer (Versioned)
│   │   └── v1/                   # API version 1 endpoints
│   │
│   ├── models/                   # Database models (SQLAlchemy ORM)
│   │   ├── booking.py, seat.py, station.py, meal.py, user.py
│   │
│   ├── schemas/                  # Pydantic schemas (Validation)
│   │   └── schemas.py            # Consolidated application schemas
│   │
│   ├── services/                 # Business logic layer
│   │   ├── booking_service.py, seat_service.py, station_service.py, prediction_service.py
│   │
│   ├── core/                     # Core utilities
│   │   └── common.py             # Consolidated exceptions & security
│   │
│   ├── ml/                       # Machine Learning System
│   │   ├── train_model.py        # Model training script
│   │   ├── predictor.py          # Inference & factor analysis
│   │   └── saved_models/         # Serialized models & encoders
│   │
│   ├── routes/                   # Custom API routes
│   │   └── prediction_routes.py  # Prediction ML endpoints
│   │
│   └── utils/                    # Helper functions
│       └── utils.py              # Consolidated validators & helpers
│
├── data/                         # Data storage
│   └── historical_bookings.csv   # Historical data for AI prediction
│
├── docs/                         # Additional documentation
│   ├── FINAL_VERIFICATION.md     # Final test results & breakdown
│   ├── PROJECT_STRUCTURE.md      # Detailed file-by-file structure
│   └── CLEANUP_SUMMARY.md        # Documentation of project cleanup
│
├── tests/                        # Test & Verification Scripts
│   ├── test_basic.py             # Basic smoke tests
│   └── test_comprehensive.py     # Full endpoint coverage tests
│
├── 📂 scripts/                      # Utility Scripts
│   └── init_db.py                # Database initialization script
│
├── requirements.txt              # Python dependencies
├── PREDICTION_APPROACH.md        # AI/ML documentation (Assignment Requirement)
└── README.md                     # This file
```

## 🏗️ Architecture Philosophy

This project prioritizes **professional software engineering practices** over minimal file count:

### Why Multiple Files?
- ✅ **Single Responsibility**: Each file and layer does ONE thing well.
- ✅ **Scalability**: New models or services can be added without bloating existing code.
- ✅ **Maintainability**: High cohesion and low coupling make the system easier to test and debug.
- ✅ **Industry Standard**: Follows recommended patterns for enterprise-scale FastAPI applications.

## 🎯 Key Features

### 1. Single Bus System
- **40 Seats**: 20 Lower Berth + 20 Upper Berth.
- **Fixed Route**: Ahmedabad → Mumbai (5 major stations).
- **Segment-based Inventory**: Real-time tracking of seat availability across different journey legs.

### 2. Advanced Booking System
- **Multi-seat Transactions**: Atomic booking process for groups.
- **Integrated Meals**: Food selection during the booking process.
- **Dynamic Pricing**: Price adjustments based on distance and seat type (Lower/Upper).

### 3. AI Prediction
- **Confirmation Probability**: Dynamic scoring (50-100%) based on booking lead time and party size.
- **Documentation**: Detailed logic in `PREDICTION_APPROACH.md`.

## 🚀 Quick Start

1. **Install Dependencies**: `pip install -r requirements.txt`
2. **Setup Database**: Update `DATABASE_URL` in `app/config.py` and run `python scripts/init_db.py`.
3. **Train Prediction Model**: `python -m app.ml.train_model`
4. **Run Server**: `uvicorn app.main:app --reload`.
5. **Access Docs**: http://localhost:8000/docs.

## 🧪 Testing

Detailed testing documentation can be found in the [tests folder](file:///d:/Sleeper-Bus-Ticket-Booking-System/tests/README.md).

- **Basic Smoke Tests**: `python tests/test_basic.py`
- **Comprehensive Tests**: `python tests/test_comprehensive.py`

## 📚 Additional Documentation
See the [docs folder](file:///d:/Sleeper-Bus-Ticket-Booking-System/docs/) for detailed records of verification, structure, and cleanup.

---
**Author**: Dhvani  
**Version**: 1.1.0 (Refactored)
