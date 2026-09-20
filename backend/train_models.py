"""Script to train ML models on historical data"""
import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

import pandas as pd
from app.database import SessionLocal
from app.models import Project
from app.ml.pipeline import MLPipeline

def prepare_training_data():
    """Prepare training data from database"""
    db = SessionLocal()
    try:
        # Get all projects (we'll use sample data structure)
        # In production, you'd have historical projects with actual team sizes and skills
        projects = db.query(Project).all()
        
        if len(projects) < 5:
            print("Not enough projects for training. Please seed data first.")
            return None
        
        # Create training dataframe
        training_data = []
        for proj in projects:
            # For training, we need to estimate team size and skills based on project characteristics
            # This is a simplified approach - in production, use actual historical data
            
            # Estimate team size based on complexity and timeline
            base_size = 2
            if proj.complexity.value == "High":
                base_size += 3
            elif proj.complexity.value == "Medium":
                base_size += 1
            
            if proj.estimated_timeline_weeks > 16:
                base_size += 1
            
            # Estimate skills based on category
            skills_map = {
                "Web": ["Python", "React", "JavaScript", "PostgreSQL", "FastAPI"],
                "AI": ["Python", "Machine Learning", "Data Analysis", "PostgreSQL"],
                "Mobile": ["Mobile Development", "React Native", "iOS", "Android"],
                "Automation": ["Python", "Automation", "RPA"],
                "ERP": ["ERP Systems", "PostgreSQL", "Python", "Integration"]
            }
            
            estimated_skills = skills_map.get(proj.category.value, ["Python", "JavaScript"])
            
            training_data.append({
                'description': proj.description,
                'category': proj.category.value,
                'complexity': proj.complexity.value,
                'client_priority': proj.client_priority.value,
                'estimated_timeline_weeks': proj.estimated_timeline_weeks,
                'team_size': base_size,
                'required_skills': estimated_skills
            })
        
        df = pd.DataFrame(training_data)
        return df
    finally:
        db.close()


def train_models():
    """Train ML models"""
    print("Preparing training data...")
    df = prepare_training_data()
    
    if df is None:
        return
    
    print(f"Training on {len(df)} projects...")
    
    # Initialize pipeline
    pipeline = MLPipeline()
    
    # Prepare features
    X, y_team_size, y_skills = pipeline.prepare_features(df)
    
    # Train team size model
    print("Training team size regression model...")
    pipeline.train_team_size_model(X, y_team_size)
    
    # Train skill classifier
    print("Training skill classification model...")
    pipeline.train_skill_classifier(X, y_skills)
    
    print("Model training completed!")


if __name__ == "__main__":
    train_models()


