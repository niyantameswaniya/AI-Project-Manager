"""Analytics and predictions API endpoints"""
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import func
from ..database import get_db
from ..models import Project, Employee
from ..schemas import AnalyticsResponse

router = APIRouter(prefix="/api/analytics", tags=["analytics"])


@router.get("/", response_model=AnalyticsResponse)
def get_analytics(db: Session = Depends(get_db)):
    """Get analytics and insights"""
    # Total projects
    total_projects = db.query(Project).count()
    
    # Total employees
    total_employees = db.query(Employee).count()
    
    # Average team size
    avg_team_size = db.query(func.avg(Project.predicted_team_size)).scalar() or 0.0
    
    # Skill distribution
    all_employees = db.query(Employee).all()
    skill_distribution = {}
    for emp in all_employees:
        for skill in emp.skills:
            skill_distribution[skill] = skill_distribution.get(skill, 0) + 1
    
    # Category distribution
    category_distribution = {}
    projects = db.query(Project).all()
    for proj in projects:
        cat = proj.category.value
        category_distribution[cat] = category_distribution.get(cat, 0) + 1
    
    return AnalyticsResponse(
        total_projects=total_projects,
        total_employees=total_employees,
        average_team_size=round(float(avg_team_size), 2),
        skill_distribution=skill_distribution,
        category_distribution=category_distribution
    )


