"""Migration script to add required_skills column to projects table"""
import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app.database import engine, SessionLocal
from sqlalchemy import text

def migrate():
    """Add required_skills column if it doesn't exist"""
    db = SessionLocal()
    try:
        # Check if column exists (SQLite specific)
        result = db.execute(text("PRAGMA table_info(projects)"))
        columns = [row[1] for row in result]
        
        if 'required_skills' not in columns:
            print("Adding required_skills column to projects table...")
            db.execute(text("ALTER TABLE projects ADD COLUMN required_skills JSON"))
            db.commit()
            print("Migration completed: required_skills column added")
        else:
            print("Column required_skills already exists")
    except Exception as e:
        print(f"Migration error: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    migrate()
