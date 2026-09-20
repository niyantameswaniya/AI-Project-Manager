"""ML Pipeline for team size prediction and skill classification"""
import pickle
import os
import numpy as np
from sklearn.ensemble import RandomForestRegressor, RandomForestClassifier
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.preprocessing import StandardScaler, MultiLabelBinarizer
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_absolute_error, accuracy_score, classification_report
import pandas as pd
from typing import List, Dict, Tuple
import joblib


class MLPipeline:
    """Machine Learning pipeline for project predictions"""
    
    def __init__(self, models_dir: str = "ml_models"):
        self.models_dir = models_dir
        os.makedirs(models_dir, exist_ok=True)
        
        # Initialize models
        self.team_size_model = RandomForestRegressor(n_estimators=100, random_state=42)
        self.skill_classifier = RandomForestClassifier(n_estimators=100, random_state=42)
        self.tfidf_vectorizer = TfidfVectorizer(max_features=100, stop_words='english')
        self.scaler = StandardScaler()
        self.skill_binarizer = MultiLabelBinarizer()
        
        # Model paths
        self.team_size_path = os.path.join(models_dir, "team_size_model.pkl")
        self.skill_classifier_path = os.path.join(models_dir, "skill_classifier.pkl")
        self.tfidf_path = os.path.join(models_dir, "tfidf_vectorizer.pkl")
        self.scaler_path = os.path.join(models_dir, "scaler.pkl")
        self.skill_binarizer_path = os.path.join(models_dir, "skill_binarizer.pkl")
    
    def prepare_features(self, df: pd.DataFrame) -> Tuple[np.ndarray, np.ndarray, np.ndarray]:
        """Prepare features from project data"""
        # Text features from description
        description_features = self.tfidf_vectorizer.fit_transform(df['description']).toarray()
        
        # Categorical features
        category_encoded = pd.get_dummies(df['category'], prefix='category')
        complexity_encoded = pd.get_dummies(df['complexity'], prefix='complexity')
        priority_encoded = pd.get_dummies(df['client_priority'], prefix='priority')
        
        # Numerical features
        numerical_features = df[['estimated_timeline_weeks']].values
        
        # Combine all features
        categorical_features = np.hstack([
            category_encoded.values,
            complexity_encoded.values,
            priority_encoded.values
        ])
        
        # Combine all features
        X = np.hstack([
            description_features,
            categorical_features,
            numerical_features
        ])
        
        # Scale features
        X_scaled = self.scaler.fit_transform(X)
        
        # Target for team size (if available)
        y_team_size = df['team_size'].values if 'team_size' in df.columns else None
        
        # Target for skills (if available)
        y_skills = df['required_skills'].values if 'required_skills' in df.columns else None
        
        return X_scaled, y_team_size, y_skills
    
    def train_team_size_model(self, X: np.ndarray, y: np.ndarray):
        """Train regression model for team size prediction"""
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=0.2, random_state=42
        )
        
        self.team_size_model.fit(X_train, y_train)
        
        # Evaluate
        y_pred = self.team_size_model.predict(X_test)
        mae = mean_absolute_error(y_test, y_pred)
        print(f"Team Size Model - MAE: {mae:.2f}")
        
        # Save model
        joblib.dump(self.team_size_model, self.team_size_path)
        print(f"Team size model saved to {self.team_size_path}")
    
    def train_skill_classifier(self, X: np.ndarray, y_skills: List[List[str]]):
        """Train multi-label classifier for skill prediction"""
        # Binarize skills
        y_binary = self.skill_binarizer.fit_transform(y_skills)
        
        X_train, X_test, y_train, y_test = train_test_split(
            X, y_binary, test_size=0.2, random_state=42
        )
        
        self.skill_classifier.fit(X_train, y_train)
        
        # Evaluate
        y_pred = self.skill_classifier.predict(X_test)
        accuracy = accuracy_score(y_test, y_pred)
        print(f"Skill Classifier - Accuracy: {accuracy:.2f}")
        
        # Save models
        joblib.dump(self.skill_classifier, self.skill_classifier_path)
        joblib.dump(self.tfidf_vectorizer, self.tfidf_path)
        joblib.dump(self.scaler, self.scaler_path)
        joblib.dump(self.skill_binarizer, self.skill_binarizer_path)
        print(f"Skill classifier saved to {self.skill_classifier_path}")
    
    def load_models(self):
        """Load trained models"""
        try:
            if os.path.exists(self.team_size_path):
                self.team_size_model = joblib.load(self.team_size_path)
            else:
                print(f"Warning: Team size model not found at {self.team_size_path}")
                
            if os.path.exists(self.skill_classifier_path):
                self.skill_classifier = joblib.load(self.skill_classifier_path)
            else:
                print(f"Warning: Skill classifier not found at {self.skill_classifier_path}")
                
            if os.path.exists(self.tfidf_path):
                self.tfidf_vectorizer = joblib.load(self.tfidf_path)
            else:
                print(f"Warning: TF-IDF vectorizer not found at {self.tfidf_path}")
                
            if os.path.exists(self.scaler_path):
                self.scaler = joblib.load(self.scaler_path)
            else:
                print(f"Warning: Scaler not found at {self.scaler_path}")
                
            if os.path.exists(self.skill_binarizer_path):
                self.skill_binarizer = joblib.load(self.skill_binarizer_path)
            else:
                print(f"Warning: Skill binarizer not found at {self.skill_binarizer_path}")
        except Exception as e:
            print(f"Error loading models: {e}")
            import traceback
            traceback.print_exc()
    
    def predict_team_size(self, project_data: Dict) -> Tuple[int, float]:
        """Predict team size for a project"""
        # Prepare single project features
        df = pd.DataFrame([project_data])
        
        # Text features
        description_features = self.tfidf_vectorizer.transform(df['description']).toarray()
        
        # Categorical features
        category_encoded = pd.get_dummies(df['category'], prefix='category')
        complexity_encoded = pd.get_dummies(df['complexity'], prefix='complexity')
        priority_encoded = pd.get_dummies(df['client_priority'], prefix='priority')
        
        # Ensure all category columns exist (handle missing categories)
        all_categories = ['category_Web', 'category_AI', 'category_Mobile', 'category_Automation', 'category_ERP']
        all_complexities = ['complexity_Low', 'complexity_Medium', 'complexity_High']
        all_priorities = ['priority_Low', 'priority_Medium', 'priority_High', 'priority_Critical']
        
        for cat in all_categories:
            if cat not in category_encoded.columns:
                category_encoded[cat] = 0
        for comp in all_complexities:
            if comp not in complexity_encoded.columns:
                complexity_encoded[comp] = 0
        for pri in all_priorities:
            if pri not in priority_encoded.columns:
                priority_encoded[pri] = 0
        
        categorical_features = np.hstack([
            category_encoded[all_categories].values,
            complexity_encoded[all_complexities].values,
            priority_encoded[all_priorities].values
        ])
        
        numerical_features = df[['estimated_timeline_weeks']].values
        
        X = np.hstack([description_features, categorical_features, numerical_features])
        X_scaled = self.scaler.transform(X)
        
        # Predict
        prediction = self.team_size_model.predict(X_scaled)[0]
        team_size = max(1, int(round(prediction)))  # Ensure at least 1 person
        
        # Calculate confidence (simplified - based on prediction variance)
        # In production, use prediction intervals
        confidence = min(0.95, max(0.5, 1 - abs(prediction - team_size) / max(team_size, 1)))
        
        return team_size, confidence
    
    def predict_skills(self, project_data: Dict) -> List[Tuple[str, float]]:
        """Predict required skills for a project"""
        # Prepare features (same as team size)
        df = pd.DataFrame([project_data])
        
        description_features = self.tfidf_vectorizer.transform(df['description']).toarray()
        
        category_encoded = pd.get_dummies(df['category'], prefix='category')
        complexity_encoded = pd.get_dummies(df['complexity'], prefix='complexity')
        priority_encoded = pd.get_dummies(df['client_priority'], prefix='priority')
        
        # Ensure all columns exist
        all_categories = ['category_Web', 'category_AI', 'category_Mobile', 'category_Automation', 'category_ERP']
        all_complexities = ['complexity_Low', 'complexity_Medium', 'complexity_High']
        all_priorities = ['priority_Low', 'priority_Medium', 'priority_High', 'priority_Critical']
        
        for cat in all_categories:
            if cat not in category_encoded.columns:
                category_encoded[cat] = 0
        for comp in all_complexities:
            if comp not in complexity_encoded.columns:
                complexity_encoded[comp] = 0
        for pri in all_priorities:
            if pri not in priority_encoded.columns:
                priority_encoded[pri] = 0
        
        categorical_features = np.hstack([
            category_encoded[all_categories].values,
            complexity_encoded[all_complexities].values,
            priority_encoded[all_priorities].values
        ])
        
        numerical_features = df[['estimated_timeline_weeks']].values
        
        X = np.hstack([description_features, categorical_features, numerical_features])
        X_scaled = self.scaler.transform(X)
        
        # Predict skill probabilities
        try:
            skill_probs = self.skill_classifier.predict_proba(X_scaled)
            
            # Handle different return formats
            if len(skill_probs.shape) > 1:
                skill_probs = skill_probs[0]
            
            # Get skill names
            if hasattr(self.skill_binarizer, 'classes_'):
                skill_names = self.skill_binarizer.classes_
            else:
                # Fallback if binarizer not properly loaded
                return []
            
            # Return skills with confidence > 0.3
            predicted_skills = []
            for i, skill in enumerate(skill_names):
                if i < len(skill_probs):
                    # Handle different probability formats
                    if isinstance(skill_probs[i], (list, np.ndarray)):
                        prob = skill_probs[i][1] if len(skill_probs[i]) > 1 else skill_probs[i][0]
                    else:
                        prob = skill_probs[i]
                    if prob > 0.3:  # Threshold for skill prediction
                        predicted_skills.append((skill, float(prob)))
            
            # Sort by confidence
            predicted_skills.sort(key=lambda x: x[1], reverse=True)
            
            return predicted_skills
        except Exception as e:
            print(f"Error in predict_skills: {e}")
            import traceback
            traceback.print_exc()
            return []

