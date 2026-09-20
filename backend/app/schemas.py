"""Pydantic schemas for request/response validation"""
from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime
from .models import ProjectCategory, ProjectComplexity, ClientPriority


# Project Schemas
class ProjectCreate(BaseModel):
    name: str = Field(..., min_length=1, max_length=255)
    description: str = Field(..., min_length=10)
    category: ProjectCategory
    complexity: ProjectComplexity
    estimated_timeline_weeks: int = Field(..., gt=0)
    budget_range: Optional[str] = None
    client_priority: ClientPriority
    required_skills: List[str] = Field(..., min_items=1, description="User-provided required skills (at least one required)")


class ProjectResponse(BaseModel):
    id: int
    name: str
    description: str
    category: ProjectCategory
    complexity: ProjectComplexity
    estimated_timeline_weeks: int
    budget_range: Optional[str]
    client_priority: ClientPriority
    required_skills: Optional[List[str]]
    predicted_team_size: Optional[int]
    predicted_skills: Optional[List[str]]
    confidence_score: Optional[float]
    created_at: datetime
    assigned_employee_ids: Optional[List[int]] = None

    class Config:
        from_attributes = True


class AssignEmployeesRequest(BaseModel):
    employee_ids: List[int] = Field(..., description="List of employee DB ids to assign to project")


# Employee Schemas
class EmployeeCreate(BaseModel):
    employee_id: str = Field(..., min_length=1, max_length=50)
    name: str = Field(..., min_length=1, max_length=255)
    email: Optional[str] = None
    department: Optional[str] = None
    location: Optional[str] = None
    designation: Optional[str] = None
    
    skills: List[str]
    skill_proficiency: List[int] = Field(..., description="Proficiency 1-5 for each skill")
    skill_types: Optional[List[str]] = Field(None, description="Technical, Soft Skills, Domain, etc.")
    
    years_of_experience: float = Field(..., ge=0)
    past_project_types: Optional[List[str]] = None
    certifications: Optional[List[str]] = None
    education: Optional[str] = None
    
    availability_percent: float = Field(100.0, ge=0, le=100)
    performance_score: float = Field(5.0, ge=1, le=10)
    hourly_rate: Optional[float] = Field(None, ge=0)
    
    languages: Optional[List[str]] = None
    frameworks: Optional[List[str]] = None
    domain_expertise: Optional[List[str]] = None


class EmployeeResponse(BaseModel):
    id: int
    employee_id: str
    name: str
    email: Optional[str]
    department: Optional[str]
    location: Optional[str]
    designation: Optional[str]
    skills: List[str]
    skill_proficiency: List[int]
    skill_types: Optional[List[str]]
    years_of_experience: float
    past_project_types: Optional[List[str]]
    certifications: Optional[List[str]]
    education: Optional[str]
    availability_percent: float
    performance_score: float
    hourly_rate: Optional[float]
    languages: Optional[List[str]]
    frameworks: Optional[List[str]]
    domain_expertise: Optional[List[str]]
    created_at: datetime

    class Config:
        from_attributes = True


# Prediction Schemas
class PredictionRequest(BaseModel):
    project_id: int


class SkillPrediction(BaseModel):
    skill: str
    confidence: float


class EmployeeMatch(BaseModel):
    employee_id: int
    employee_name: str
    employee_employee_id: str
    match_score: float
    match_reason: str
    skills_match: List[str]
    missing_skills: List[str]
    department: Optional[str] = None
    designation: Optional[str] = None
    years_experience: Optional[float] = None
    certifications: Optional[List[str]] = None


class PredictionResponse(BaseModel):
    project_id: int
    predicted_team_size: int
    predicted_skills: List[SkillPrediction]
    recommended_employees: List[EmployeeMatch]
    missing_skills: List[str]
    confidence_score: float
    explanation: str


# Analytics Schemas
class AnalyticsResponse(BaseModel):
    total_projects: int
    total_employees: int
    average_team_size: float
    skill_distribution: dict
    category_distribution: dict


