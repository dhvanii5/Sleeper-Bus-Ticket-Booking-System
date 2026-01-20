"""
Database initialization script for Sleeper Bus Ticket Booking System
"""
import sys
from pathlib import Path

# Add project root to Python path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

from app.database import engine, Base
# Import all models to register them with Base
import app.models.user
import app.models.booking
import app.models.meal
import app.models.seat
import app.models.station

def init_database():
    """
    Create all database tables based on SQLAlchemy models
    """
    try:
        print("=" * 50)
        print("🚀 Starting Database Initialization...")
        print("=" * 50)
        
        # Create all tables
        Base.metadata.create_all(bind=engine)
        
        print("\n✅ Database tables created successfully!\n")
        print("Tables created:")
        print("  📋 users")
        print("  🎫 bookings")
        print("  🍽️  meals")
        print("  💺 seats")
        print("  🚉 stations")
        print("\n" + "=" * 50)
        print("✨ Database setup complete!")
        print("=" * 50)
        
    except Exception as e:
        print(f"\n❌ Error creating database tables: {e}")
        print(f"\nDetails: {type(e).__name__}")
        sys.exit(1)

if __name__ == "__main__":
    init_database()