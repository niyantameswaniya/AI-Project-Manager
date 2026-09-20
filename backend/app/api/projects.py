"""Project management API endpoints"""
import numpy as np
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from ..database import get_db
from ..models import Project, EmployeeAssignment, Employee
from ..schemas import ProjectCreate, ProjectResponse, AssignEmployeesRequest
from ..ml.pipeline import MLPipeline
from ..ml.matching import EmployeeMatchingEngine
from ..schemas import PredictionResponse, SkillPrediction, EmployeeMatch

router = APIRouter(prefix="/api/projects", tags=["projects"])

# Initialize ML components
ml_pipeline = MLPipeline()
ml_pipeline.load_models()
matching_engine = EmployeeMatchingEngine()


@router.post("/", response_model=ProjectResponse, status_code=201)
def create_project(project: ProjectCreate, db: Session = Depends(get_db)):
    """Create a new project"""
    try:
        db_project = Project(**project.dict())
        db.add(db_project)
        db.commit()
        db.refresh(db_project)
        return db_project
    except Exception as e:
        db.rollback()
        print(f"Error creating project: {str(e)}")
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=400, detail=f"Error creating project: {str(e)}")


@router.get("/", response_model=List[ProjectResponse])
def get_projects(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """Get all projects"""
    projects = db.query(Project).offset(skip).limit(limit).all()
    return projects


@router.get("/{project_id}", response_model=ProjectResponse)
def get_project(project_id: int, db: Session = Depends(get_db)):
    """Get a specific project"""
    project = db.query(Project).filter(Project.id == project_id).first()
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    return project


@router.post("/{project_id}/assign", response_model=ProjectResponse)
def assign_employees_to_project(
    project_id: int,
    body: AssignEmployeesRequest,
    db: Session = Depends(get_db),
):
    """Manager confirms employees for this project. Creates assignments."""
    project = db.query(Project).filter(Project.id == project_id).first()
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    existing_ids = {a.employee_id for a in project.employee_assignments}
    for eid in body.employee_ids:
        if eid in existing_ids:
            continue
        emp = db.query(Employee).filter(Employee.id == eid).first()
        if not emp:
            raise HTTPException(status_code=400, detail=f"Employee id {eid} not found")
        db.add(
            EmployeeAssignment(
                project_id=project_id,
                employee_id=eid,
                match_score=0.0,
                match_reason="Confirmed by manager",
            )
        )
        existing_ids.add(eid)
    db.commit()
    db.refresh(project)
    return project


@router.post("/{project_id}/predict", response_model=PredictionResponse)
def predict_project_requirements(project_id: int, db: Session = Depends(get_db)):
    """Generate ML predictions for a project"""
    try:
        project = db.query(Project).filter(Project.id == project_id).first()
        if not project:
            raise HTTPException(status_code=404, detail="Project not found")
        
        # Prepare project data for ML
        project_data = {
            'description': project.description,
            'category': project.category.value,
            'complexity': project.complexity.value,
            'client_priority': project.client_priority.value,
            'estimated_timeline_weeks': project.estimated_timeline_weeks
        }
        
        # Predict team size
        try:
            team_size, team_confidence = ml_pipeline.predict_team_size(project_data)
        except Exception as e:
            # Fallback if ML model fails
            print(f"Team size prediction error: {e}")
            team_size = 3  # Default team size
            team_confidence = 0.7
        
        # Get required skills - combine user-provided and ML-predicted
        user_provided_skills = project.required_skills or []
        
        # Predict required skills using ML
        try:
            skill_predictions = ml_pipeline.predict_skills(project_data)
            ml_predicted_skills = [skill for skill, conf in skill_predictions]
        except Exception as e:
            # Fallback if skill prediction fails
            print(f"Skill prediction error: {e}")
            skill_predictions = []
            ml_predicted_skills = []
        
        # Combine user-provided and ML-predicted skills (remove duplicates)
        all_required_skills = list(set(user_provided_skills + ml_predicted_skills))
        required_skills = all_required_skills
        
        # Ensure we have at least user-provided skills even if ML fails
        if not required_skills and user_provided_skills:
            required_skills = user_provided_skills
        
        # Find best employee matches
        try:
            employee_matches = matching_engine.find_best_matches(
                db=db,
                required_skills=required_skills,
                project_category=project.category.value,
                project_complexity=project.complexity.value,
                team_size=team_size
            )
        except Exception as e:
            print(f"Employee matching error: {e}")
            employee_matches = []
        
        # Calculate overall confidence
        skill_confidences = [conf for _, conf in skill_predictions]
        avg_skill_confidence = np.mean(skill_confidences) if skill_confidences else 0.5
        overall_confidence = (team_confidence * 0.4 + avg_skill_confidence * 0.6)
        
        # Collect missing skills - only skills that are truly missing across ALL recommended employees
        # If a skill (or its alias) is matched by at least one employee, it's not missing
        from ..ml.matching import EmployeeMatchingEngine
        temp_engine = EmployeeMatchingEngine()
        
        # Collect all matched skills from all employees (normalized to lowercase for comparison)
        all_matched_skills_normalized = set()
        for match in employee_matches:
            for matched_skill in match.get('skills_match', []):
                # Get all variations of the matched skill
                variations = temp_engine.normalize_skill_for_matching(matched_skill)
                all_matched_skills_normalized.update([v.lower() for v in variations])
        
        # Check which required skills are truly missing (considering aliases)
        all_required_skills_set = set(required_skills)
        truly_missing = []
        
        for req_skill in all_required_skills_set:
            req_variations = temp_engine.normalize_skill_for_matching(req_skill)
            req_variations_lower = {v.lower() for v in req_variations}
            
            # Check if any variation of this required skill was matched
            if not req_variations_lower.intersection(all_matched_skills_normalized):
                truly_missing.append(req_skill)
        
        all_missing_skills = truly_missing
        
        # Update project with predictions
        project.predicted_team_size = team_size
        project.predicted_skills = required_skills
        project.confidence_score = overall_confidence
        db.commit()
        
        # Format response - include both user-provided and ML-predicted skills
        skill_predictions_formatted = []
        
        # Add user-provided skills first (with 100% confidence since user specified them)
        for skill in user_provided_skills:
            skill_predictions_formatted.append(
                SkillPrediction(skill=skill, confidence=100.0)
            )
        
        # Add ML-predicted skills (avoid duplicates)
        user_skills_lower = [s.lower() for s in user_provided_skills]
        for skill, conf in skill_predictions:
            if skill.lower() not in user_skills_lower:
                skill_predictions_formatted.append(
                    SkillPrediction(skill=skill, confidence=round(conf * 100, 2))
                )
        
        employee_matches_formatted = [
            EmployeeMatch(**match) for match in employee_matches
        ]
        
        # Build explanation
        user_skills_count = len(user_provided_skills)
        ml_skills_count = len(ml_predicted_skills)
        
        if user_skills_count > 0 and ml_skills_count > 0:
            explanation = (
                f"Based on the project requirements, we predict a team size of {team_size} employees. "
                f"You provided {user_skills_count} required skill(s), and the AI model identified {ml_skills_count} additional skill(s). "
                f"Total {len(required_skills)} unique skills are considered for employee matching. "
                f"Top matches were selected based on skill alignment, experience relevance, availability, and performance."
            )
        elif user_skills_count > 0:
            explanation = (
                f"Based on the project requirements, we predict a team size of {team_size} employees. "
                f"Using the {user_skills_count} required skill(s) you provided for employee matching. "
                f"Top matches were selected based on skill alignment, experience relevance, availability, and performance."
            )
        elif ml_skills_count > 0:
            explanation = (
                f"Based on the project requirements, we predict a team size of {team_size} employees. "
                f"The AI model identified {ml_skills_count} key skill(s) needed for this project. "
                f"Top matches were selected based on skill alignment, experience relevance, availability, and performance."
            )
        else:
            explanation = (
                f"Based on the project requirements, we predict a team size of {team_size} employees. "
                f"Top matches were selected based on experience relevance, availability, and performance."
            )
        
        return PredictionResponse(
            project_id=project_id,
            predicted_team_size=team_size,
            predicted_skills=skill_predictions_formatted,
            recommended_employees=employee_matches_formatted,
            missing_skills=list(all_missing_skills),
            confidence_score=round(overall_confidence * 100, 2),
            explanation=explanation
        )
    except HTTPException:
        raise
    except Exception as e:
        print(f"Prediction error: {str(e)}")
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=f"Error generating prediction: {str(e)}")

