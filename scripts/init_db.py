"""
Database initialization script for Sleeper Bus Ticket Booking System
"""
import sys
from pathlib import Path

# Add project root to Python path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from app.database import engine, Base, SessionLocal
from app.config import STATIONS, BUS_CONFIG
# Import all models to register them with Base
from app.models.user import User
from app.models.booking import Booking, BookingMeal
from app.models.meal import Meal
from app.models.seat import Seat
from app.models.station import Station

def init_database():
    """
    Create all database tables and seed initial data
    """
    try:
        print("=" * 50)
        print("🚀 Starting Database Initialization...")
        print("=" * 50)
        
        # Create all tables
        Base.metadata.drop_all(bind=engine) # Drop all to ensure clean slate for hardcoded constraints
        Base.metadata.create_all(bind=engine)
        
        print("\n✅ Database tables created successfully!")
        
        # Seed Data
        db = SessionLocal()
        
        # 1. Seed Stations
        print("\n📍 Seeding Stations...")
        for station_data in STATIONS:
            station = Station(
                name=station_data["name"],
                sequence=station_data["sequence"],
                arrival_time=station_data["arrival_time"],
                departure_time=station_data["departure_time"],
                distance_km=station_data["distance_km"]
            )
            db.add(station)
        
        # 2. Seed Seats
        print("\n💺 Seeding Seats...")
        # Lower Berth (S01 - S20)
        for i in range(1, 21):
            seat = Seat(
                seat_number=f"S{i:02d}",
                seat_type="lower",
                base_price=800,  # Base price, can be dynamic later
                is_available=True
            )
            db.add(seat)
            
        # Upper Berth (S21 - S40)
        for i in range(21, 41):
            seat = Seat(
                seat_number=f"S{i:02d}",
                seat_type="upper",
                base_price=700, # Upper berths usually cheaper
                is_available=True
            )
            db.add(seat)
            
        # 3. Seed Meals
        print("\n🍽️  Seeding Meals...")
        meals_data = [
            {"name": "Veg Thali", "price": 150, "type": "veg", "description": "Complete meal with Roti, Paneer, Dal, Rice, Salad"},
            {"name": "Chicken Biryani", "price": 250, "type": "non-veg", "description": "Authentic Hyderabadi Chicken Biryani with Raita"},
            {"name": "Sandwich Combo", "price": 100, "type": "veg", "description": "Grilled sandwich with chips and juice"},
            {"name": "Water Bottle", "price": 20, "type": "veg", "description": "1 Litre Mineral Water"},
            {"name": "Masala Chai", "price": 30, "type": "veg", "description": "Hot Spiced Tea"}
        ]
        
        for meal_data in meals_data:
            meal = Meal(
                name=meal_data["name"],
                price=meal_data["price"],
                category=meal_data["type"], # Mapping type to category
                description=meal_data["description"],
                is_available=True
            )
            db.add(meal)
            
        db.commit()
        db.close()
        
        print("\n✅ Data Seeding Completed!")
        print(f"   - {len(STATIONS)} Stations added")
        print(f"   - {BUS_CONFIG['total_seats']} Seats added")
        print(f"   - {len(meals_data)} Meals added")
        
        print("\n" + "=" * 50)
        print("✨ Database setup complete!")
        print("=" * 50)
        
    except Exception as e:
        print(f"\n❌ Error creating database tables: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

if __name__ == "__main__":
    init_database()