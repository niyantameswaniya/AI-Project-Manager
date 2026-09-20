"""Employee management API endpoints"""
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from ..database import get_db
from ..models import Employee, EmployeeAssignment
from ..schemas import EmployeeCreate, EmployeeResponse
from ..schemas import ProjectResponse

router = APIRouter(prefix="/api/employees", tags=["employees"])


@router.post("/", response_model=EmployeeResponse, status_code=201)
def create_employee(employee: EmployeeCreate, db: Session = Depends(get_db)):
    """Create a new employee"""
    # Validate skills and proficiencies match
    if len(employee.skills) != len(employee.skill_proficiency):
        raise HTTPException(
            status_code=400,
            detail="Number of skills must match number of skill proficiencies"
        )
    
    # Check if employee_id already exists
    existing = db.query(Employee).filter(Employee.employee_id == employee.employee_id).first()
    if existing:
        raise HTTPException(
            status_code=400,
            detail=f"Employee with ID {employee.employee_id} already exists"
        )
    
    db_employee = Employee(**employee.dict())
    db.add(db_employee)
    db.commit()
    db.refresh(db_employee)
    return db_employee


@router.get("/", response_model=List[EmployeeResponse])
def get_employees(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """Get all employees"""
    employees = db.query(Employee).offset(skip).limit(limit).all()
    return employees


@router.get("/{employee_id}", response_model=EmployeeResponse)
def get_employee(employee_id: int, db: Session = Depends(get_db)):
    """Get a specific employee by database ID"""
    employee = db.query(Employee).filter(Employee.id == employee_id).first()
    if not employee:
        raise HTTPException(status_code=404, detail="Employee not found")
    return employee


@router.get("/by-employee-id/{employee_identifier}", response_model=EmployeeResponse)
def get_employee_by_identifier(employee_identifier: str, db: Session = Depends(get_db)):
    """Get a specific employee by employee_id field"""
    employee = db.query(Employee).filter(Employee.employee_id == employee_identifier).first()
    if not employee:
        raise HTTPException(status_code=404, detail="Employee not found")
    return employee


@router.get("/{employee_id}/projects", response_model=List[ProjectResponse])
def get_employee_projects(employee_id: int, db: Session = Depends(get_db)):
    """Get all projects assigned to this employee (for employee view)."""
    employee = db.query(Employee).filter(Employee.id == employee_id).first()
    if not employee:
        raise HTTPException(status_code=404, detail="Employee not found")
    assignments = db.query(EmployeeAssignment).filter(EmployeeAssignment.employee_id == employee_id).all()
    projects = [a.project for a in assignments]
    return projects


