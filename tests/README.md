# Tests Directory

This directory contains verification scripts for the Sleeper Bus Ticket Booking System.

## 🚀 How to Run Tests

### 1. Basic Smoke Tests
Run this for a quick verification of core functionality (stations, seats, basic booking).
```bash
python tests/test_basic.py
```

### 2. Comprehensive Endpoint Testing
Run this for a full verification of all endpoints, atomic transactions, and edge cases.
```bash
python tests/test_comprehensive.py
```

## 📋 Test Coverage
- **test_basic.py**: Focuses on "happy path" and system initialization.
- **test_comprehensive.py**: Tests complex scenarios like overlapping segments, refund calculations, and invalid data rejection.

## 🔧 Prerequisites
- Ensure the database is initialized: `python init_db.py`
- Most tests use `TestClient`, so the server doesn't need to be running separately, but it's recommended to have your environment set up.
