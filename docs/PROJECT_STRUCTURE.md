# Complete Project Structure - Sleeper Bus Ticket Booking System

## 📁 Directory Tree

```
Sleeper-Bus-Ticket-Booking-System/
│
├── 📄 README.md                        # Professional documentation & Setup
├── 📄 PREDICTION_APPROACH.md          # AI logic documentation
├── 📄 requirements.txt                 # Project dependencies
├── 📂 scripts/                       # Utility Scripts
│   └── init_db.py                    # Database setup script
│
├── 📂 app/                            # Core Application
│   ├── 📄 main.py                    # Entry point & Routing
│   ├── 📄 config.py                  # Global settings
│   ├── 📄 database.py                # Persistence setup
│   │
│   ├── 📂 api/v1/                     # API Endpoints
│   │   └── bookings.py, seats.py, stations.py, meals.py, predictions.py
│   │
│   ├── 📂 models/                     # Data Models
│   │   └── booking.py, seat.py, station.py, meal.py
│   │
│   ├── 📂 services/                   # Business Logic
│   │   └── booking_service.py, seat_service.py, prediction_service.py
│   │
│   ├── 📂 schemas/                    # Pydantic Schemas
│   │   └── schemas.py                # Consolidated schemas
│   │
│   ├── 📂 core/                       # Shared Domain logic
│   │   └── common.py                 # Merged Exceptions & Security
│   │
│   └── 📂 utils/                      # Helper logic
│       └── utils.py                  # Merged Validators & Helpers
│
├── 📂 data/                           # Data Storage
│   └── historical_bookings.csv       # Training data for AI
│
├── 📂 docs/                           # Documentation Vault
│   ├── FINAL_VERIFICATION.md         # Detailed test reports
│   ├── PROJECT_STRUCTURE.md          # [THIS FILE]
│   └── CLEANUP_SUMMARY.md            # Maintenance records
│
└── 📂 tests/                          # Quality Assurance
    ├── test_basic.py                 # Smoke tests
    └── test_comprehensive.py         # Full system tests
```

## 📋 Layer Descriptions

### 🚀 API Layer (`app/api/`)
Handles HTTP requests and responses. Uses dependency injection for session management.
- **Bookings**: Life-cycle management of tickets.
- **Seats**: Real-time availability checks.

### 🧠 Service Layer (`app/services/`)
Orchestrates business logic. Isolates complex rules from the API controllers.
- **Booking Service**: Manages multi-seat logic and atomic saves.
- **Prediction Service**: Heuristic-based confirmation probability.

### 🏛️ Model Layer (`app/models/`)
Defines the database schema using SQLAlchemy ORM.
- **Segmented Inventory**: `SeatAvailability` tracks bookings per station-to-station leg.

### 🛡️ Core & Utils
- **Common**: Centralized error management and security (PNR/Ref generation).
- **Utils**: Reusable logic for pricing, validation, and date handling.

---
**Maintained by**: Dhvani  
**Last Updated**: January 2026
