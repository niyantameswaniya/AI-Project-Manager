"""SQLAlchemy database models"""
from sqlalchemy import Column, Integer, String, Float, Text, DateTime, ForeignKey, Enum as SQLEnum, JSON
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from .database import Base
import enum
import json


class ProjectCategory(str, enum.Enum):
    WEB = "Web"
    AI = "AI"
    MOBILE = "Mobile"
    AUTOMATION = "Automation"
    ERP = "ERP"


class ProjectComplexity(str, enum.Enum):
    LOW = "Low"
    MEDIUM = "Medium"
    HIGH = "High"


class ClientPriority(str, enum.Enum):
    LOW = "Low"
    MEDIUM = "Medium"
    HIGH = "High"
    CRITICAL = "Critical"


class Project(Base):
    __tablename__ = "projects"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False, index=True)
    description = Column(Text, nullable=False)
    category = Column(SQLEnum(ProjectCategory), nullable=False)
    complexity = Column(SQLEnum(ProjectComplexity), nullable=False)
    estimated_timeline_weeks = Column(Integer, nullable=False)
    budget_range = Column(String(100), nullable=True)
    client_priority = Column(SQLEnum(ClientPriority), nullable=False)
    required_skills = Column(JSON, nullable=True)  # User-provided skills
    skill_priorities = Column(JSON, nullable=True)  # Which skills are must-have vs nice-to-have
    team_structure = Column(String(100), nullable=True)  # Agile, Waterfall, Hybrid
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    # ML Prediction Results
    predicted_team_size = Column(Integer, nullable=True)
    predicted_skills = Column(JSON, nullable=True)  # JSON for SQLite compatibility
    confidence_score = Column(Float, nullable=True)

    # Relationships
    employee_assignments = relationship("EmployeeAssignment", back_populates="project")

    @property
    def assigned_employee_ids(self):
        return [a.employee_id for a in self.employee_assignments]


class Employee(Base):
    __tablename__ = "employees"

    id = Column(Integer, primary_key=True, index=True)
    employee_id = Column(String(50), unique=True, nullable=False, index=True)
    name = Column(String(255), nullable=False)
    email = Column(String(255), nullable=True)
    department = Column(String(100), nullable=True)  # Engineering, Data Science, Design, etc.
    location = Column(String(100), nullable=True)  # Office location or remote
    designation = Column(String(100), nullable=True)  # Senior Developer, Lead, etc.
    
    # Skills with types
    skills = Column(JSON, nullable=False)  # List of skill names
    skill_proficiency = Column(JSON, nullable=False)  # Proficiency 1-5 for each skill
    skill_types = Column(JSON, nullable=True)  # Technical, Soft Skills, Domain, etc. for each skill
    
    # Experience and background
    years_of_experience = Column(Float, nullable=False)
    past_project_types = Column(JSON, nullable=True)
    certifications = Column(JSON, nullable=True)  # List of certifications
    education = Column(String(255), nullable=True)  # Degree/Education level
    
    # Availability and performance
    availability_percent = Column(Float, nullable=False, default=100.0)
    performance_score = Column(Float, nullable=False, default=5.0)  # 1-10 scale
    hourly_rate = Column(Float, nullable=True)  # Optional billing rate
    
    # Additional metadata
    languages = Column(JSON, nullable=True)  # Programming languages known
    frameworks = Column(JSON, nullable=True)  # Frameworks/tools expertise
    domain_expertise = Column(JSON, nullable=True)  # Industry domains (Finance, Healthcare, etc.)
    
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    # Relationships
    assignments = relationship("EmployeeAssignment", back_populates="employee")


class EmployeeAssignment(Base):
    __tablename__ = "employee_assignments"

    id = Column(Integer, primary_key=True, index=True)
    project_id = Column(Integer, ForeignKey("projects.id"), nullable=False)
    employee_id = Column(Integer, ForeignKey("employees.id"), nullable=False)
    match_score = Column(Float, nullable=False)
    match_reason = Column(Text, nullable=True)
    assigned_at = Column(DateTime(timezone=True), server_default=func.now())

    # Relationships
    project = relationship("Project", back_populates="employee_assignments")
    employee = relationship("Employee", back_populates="assignments")


class MLModel(Base):
    __tablename__ = "ml_models"

    id = Column(Integer, primary_key=True, index=True)
    model_name = Column(String(100), nullable=False)
    model_type = Column(String(50), nullable=False)  # 'team_size', 'skill_classification', 'matching'
    model_path = Column(String(255), nullable=False)
    accuracy = Column(Float, nullable=True)
    trained_at = Column(DateTime(timezone=True), server_default=func.now())
    version = Column(String(20), nullable=False, default="1.0")

