"""Migration script to add new project fields"""
import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app.database import engine, SessionLocal
from sqlalchemy import text

def migrate():
    """Add new project fields if they don't exist"""
    db = SessionLocal()
    try:
        result = db.execute(text("PRAGMA table_info(projects)"))
        columns = [row[1] for row in result]
        
        new_fields = [
            ("skill_priorities", "JSON"),
            ("team_structure", "VARCHAR(100)"),
        ]
        
        added_count = 0
        for field_name, field_type in new_fields:
            if field_name not in columns:
                print(f"Adding {field_name} column to projects table...")
                db.execute(text(f"ALTER TABLE projects ADD COLUMN {field_name} {field_type}"))
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
