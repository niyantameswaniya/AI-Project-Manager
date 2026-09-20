"""Script to clear all projects from the database"""
import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app.database import SessionLocal
from app.models import Project

def clear_all_projects(confirm=True):
    """Delete all projects from the database"""
    db = SessionLocal()
    try:
        projects = db.query(Project).all()
        count = len(projects)
        
        if count == 0:
            print("No projects found in database.")
            return
        
        print(f"Found {count} project(s) in database.")
        
        if confirm:
            response = input(f"Are you sure you want to delete all {count} project(s)? (yes/no): ")
            if response.lower() != 'yes':
                print("Operation cancelled.")
                return
        
        db.query(Project).delete()
        db.commit()
        print(f"Successfully deleted {count} project(s) from the database.")
    except Exception as e:
        print(f"Error clearing projects: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    import sys
    # If --yes flag is passed, skip confirmation
    auto_confirm = '--yes' in sys.argv
    clear_all_projects(confirm=not auto_confirm)
