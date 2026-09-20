"""Migration script to add new employee fields"""
import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app.database import engine, SessionLocal
from sqlalchemy import text

def migrate():
    """Add new employee fields if they don't exist"""
    db = SessionLocal()
    try:
        # Check existing columns
        result = db.execute(text("PRAGMA table_info(employees)"))
        columns = [row[1] for row in result]
        
        new_fields = [
            ("email", "VARCHAR(255)"),
            ("department", "VARCHAR(100)"),
            ("location", "VARCHAR(100)"),
            ("designation", "VARCHAR(100)"),
            ("skill_types", "JSON"),
            ("certifications", "JSON"),
            ("education", "VARCHAR(255)"),
            ("hourly_rate", "FLOAT"),
            ("languages", "JSON"),
            ("frameworks", "JSON"),
            ("domain_expertise", "JSON"),
        ]
        
        added_count = 0
        for field_name, field_type in new_fields:
            if field_name not in columns:
                print(f"Adding {field_name} column to employees table...")
                db.execute(text(f"ALTER TABLE employees ADD COLUMN {field_name} {field_type}"))
                added_count += 1
        
        db.commit()
        if added_count > 0:
            print(f"Migration completed: {added_count} new columns added")
        else:
            print("All columns already exist")
    except Exception as e:
        print(f"Migration error: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    migrate()
