"""Seed script to populate database with sample data for ML training"""
import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app.database import SessionLocal, init_db
from app.models import Project, Employee, ProjectCategory, ProjectComplexity, ClientPriority
import random

# Sample skills pool
ALL_SKILLS = [
    "Python", "JavaScript", "React", "Node.js", "FastAPI", "Django",
    "Machine Learning", "Deep Learning", "TensorFlow", "PyTorch",
    "PostgreSQL", "MongoDB", "Redis", "Docker", "Kubernetes",
    "AWS", "Azure", "GCP", "CI/CD", "Git",
    "Mobile Development", "iOS", "Android", "Flutter", "React Native",
    "UI/UX Design", "Figma", "Adobe XD", "Web Design",
    "Automation", "RPA", "Selenium", "Test Automation",
    "ERP Systems", "SAP", "Oracle", "Salesforce",
    "Data Analysis", "SQL", "Pandas", "NumPy", "Data Visualization"
]

# Sample project categories
CATEGORIES = ["Web", "AI", "Mobile", "Automation", "ERP"]

# Sample complexities
COMPLEXITIES = ["Low", "Medium", "High"]

# Sample priorities
PRIORITIES = ["Low", "Medium", "High", "Critical"]


def create_sample_projects(db):
    """Create sample projects with historical data for ML training"""
    sample_projects = [
        {
            "name": "E-commerce Platform Redesign",
            "description": "Complete redesign of e-commerce platform with modern UI, payment integration, and inventory management system. Requires responsive design and mobile optimization.",
            "category": ProjectCategory.WEB,
            "complexity": ProjectComplexity.HIGH,
            "estimated_timeline_weeks": 16,
            "budget_range": "$100k-$150k",
            "client_priority": ClientPriority.HIGH,
            "team_size": 5,
            "required_skills": ["Python", "React", "PostgreSQL", "JavaScript", "UI/UX Design"]
        },
        {
            "name": "AI Chatbot for Customer Support",
            "description": "Develop intelligent chatbot using NLP and machine learning for automated customer support. Integration with existing CRM system.",
            "category": ProjectCategory.AI,
            "complexity": ProjectComplexity.HIGH,
            "estimated_timeline_weeks": 12,
            "budget_range": "$80k-$120k",
            "client_priority": ClientPriority.CRITICAL,
            "team_size": 4,
            "required_skills": ["Python", "Machine Learning", "NLP", "FastAPI", "PostgreSQL"]
        },
        {
            "name": "Mobile Banking App",
            "description": "Native mobile application for banking services with secure authentication, transaction history, and bill payments.",
            "category": ProjectCategory.MOBILE,
            "complexity": ProjectComplexity.HIGH,
            "estimated_timeline_weeks": 20,
            "budget_range": "$150k-$200k",
            "client_priority": ClientPriority.CRITICAL,
            "team_size": 6,
            "required_skills": ["Mobile Development", "iOS", "Android", "React Native", "PostgreSQL", "Security"]
        },
        {
            "name": "Data Entry Automation",
            "description": "Automate repetitive data entry tasks using RPA tools. Process invoices and update ERP system automatically.",
            "category": ProjectCategory.AUTOMATION,
            "complexity": ProjectComplexity.MEDIUM,
            "estimated_timeline_weeks": 8,
            "budget_range": "$40k-$60k",
            "client_priority": ClientPriority.MEDIUM,
            "team_size": 2,
            "required_skills": ["Automation", "RPA", "Python", "ERP Systems"]
        },
        {
            "name": "ERP System Integration",
            "description": "Integrate multiple business systems with central ERP platform. Data migration and workflow automation.",
            "category": ProjectCategory.ERP,
            "complexity": ProjectComplexity.HIGH,
            "estimated_timeline_weeks": 24,
            "budget_range": "$200k-$300k",
            "client_priority": ClientPriority.HIGH,
            "team_size": 8,
            "required_skills": ["ERP Systems", "SAP", "PostgreSQL", "Python", "Integration", "Data Migration"]
        },
        {
            "name": "Corporate Website",
            "description": "Modern corporate website with CMS, blog functionality, and contact forms. SEO optimized.",
            "category": ProjectCategory.WEB,
            "complexity": ProjectComplexity.LOW,
            "estimated_timeline_weeks": 6,
            "budget_range": "$20k-$30k",
            "client_priority": ClientPriority.LOW,
            "team_size": 2,
            "required_skills": ["JavaScript", "React", "Web Design", "UI/UX Design"]
        },
        {
            "name": "Predictive Analytics Dashboard",
            "description": "Build ML-powered analytics dashboard for sales forecasting and customer behavior prediction.",
            "category": ProjectCategory.AI,
            "complexity": ProjectComplexity.HIGH,
            "estimated_timeline_weeks": 14,
            "budget_range": "$90k-$130k",
            "client_priority": ClientPriority.HIGH,
            "team_size": 5,
            "required_skills": ["Python", "Machine Learning", "Data Analysis", "React", "PostgreSQL", "Data Visualization"]
        },
        {
            "name": "Fitness Tracking Mobile App",
            "description": "Cross-platform mobile app for fitness tracking with workout plans, progress charts, and social features.",
            "category": ProjectCategory.MOBILE,
            "complexity": ProjectComplexity.MEDIUM,
            "estimated_timeline_weeks": 12,
            "budget_range": "$60k-$90k",
            "client_priority": ClientPriority.MEDIUM,
            "team_size": 4,
            "required_skills": ["Mobile Development", "React Native", "PostgreSQL", "UI/UX Design"]
        },
        {
            "name": "Email Marketing Automation",
            "description": "Automate email campaigns with personalized content, A/B testing, and analytics integration.",
            "category": ProjectCategory.AUTOMATION,
            "complexity": ProjectComplexity.MEDIUM,
            "estimated_timeline_weeks": 10,
            "budget_range": "$50k-$70k",
            "client_priority": ClientPriority.MEDIUM,
            "team_size": 3,
            "required_skills": ["Python", "Automation", "PostgreSQL", "API Integration"]
        },
        {
            "name": "Inventory Management System",
            "description": "Web-based inventory management with real-time tracking, reporting, and supplier integration.",
            "category": ProjectCategory.WEB,
            "complexity": ProjectComplexity.MEDIUM,
            "estimated_timeline_weeks": 10,
            "budget_range": "$70k-$100k",
            "client_priority": ClientPriority.HIGH,
            "team_size": 4,
            "required_skills": ["Python", "React", "PostgreSQL", "FastAPI", "Web Design"]
        }
    ]
    
    for proj_data in sample_projects:
        # Remove team_size and required_skills (not in model)
        project_dict = {k: v for k, v in proj_data.items() if k not in ['team_size', 'required_skills']}
        project = Project(**project_dict)
        db.add(project)
    
    db.commit()
    print(f"Created {len(sample_projects)} sample projects")


def create_sample_employees(db):
    """Create sample employees with diverse skills and enhanced details"""
    sample_employees = [
        {
            "employee_id": "EMP001",
            "name": "Sarah Johnson",
            "email": "sarah.johnson@company.com",
            "department": "Engineering",
            "location": "San Francisco",
            "designation": "Senior Backend Developer",
            "skills": ["Python", "FastAPI", "PostgreSQL", "Docker", "AWS"],
            "skill_proficiency": [5, 5, 4, 4, 4],
            "skill_types": ["Technical", "Technical", "Technical", "Technical", "Technical"],
            "years_of_experience": 8.5,
            "past_project_types": ["Web", "AI"],
            "certifications": ["AWS Certified Solutions Architect", "Python Professional"],
            "education": "M.S. Computer Science",
            "availability_percent": 85.0,
            "performance_score": 9.2,
            "languages": ["Python", "JavaScript", "Go"],
            "frameworks": ["FastAPI", "Django", "Flask"],
            "domain_expertise": ["E-commerce", "FinTech"]
        },
        {
            "employee_id": "EMP002",
            "name": "Michael Chen",
            "email": "michael.chen@company.com",
            "department": "Data Science",
            "location": "New York",
            "designation": "Lead ML Engineer",
            "skills": ["Machine Learning", "Python", "TensorFlow", "Data Analysis", "Pandas"],
            "skill_proficiency": [5, 5, 5, 5, 5],
            "skill_types": ["Technical", "Technical", "Technical", "Technical", "Technical"],
            "years_of_experience": 10.0,
            "past_project_types": ["AI"],
            "certifications": ["TensorFlow Developer Certificate", "AWS ML Specialty"],
            "education": "Ph.D. Machine Learning",
            "availability_percent": 70.0,
            "performance_score": 9.5,
            "languages": ["Python", "R", "Scala"],
            "frameworks": ["TensorFlow", "PyTorch", "Scikit-learn"],
            "domain_expertise": ["Healthcare AI", "Predictive Analytics"]
        },
        {
            "employee_id": "EMP003",
            "name": "Emily Rodriguez",
            "email": "emily.rodriguez@company.com",
            "department": "Engineering",
            "location": "Austin",
            "designation": "Senior Frontend Developer",
            "skills": ["React", "JavaScript", "Node.js", "UI/UX Design", "Figma"],
            "skill_proficiency": [5, 5, 4, 5, 4],
            "skill_types": ["Technical", "Technical", "Technical", "Design", "Design"],
            "years_of_experience": 6.0,
            "past_project_types": ["Web", "Mobile"],
            "certifications": ["React Professional", "UI/UX Design Certificate"],
            "education": "B.S. Computer Science",
            "availability_percent": 90.0,
            "performance_score": 8.8,
            "languages": ["JavaScript", "TypeScript", "HTML/CSS"],
            "frameworks": ["React", "Next.js", "Vue.js"],
            "domain_expertise": ["SaaS", "E-commerce"]
        },
        {
            "employee_id": "EMP004",
            "name": "David Kim",
            "email": "david.kim@company.com",
            "department": "Engineering",
            "location": "Seattle",
            "designation": "Mobile Development Lead",
            "skills": ["Mobile Development", "iOS", "Android", "React Native", "Flutter"],
            "skill_proficiency": [5, 5, 4, 5, 4],
            "skill_types": ["Technical", "Technical", "Technical", "Technical", "Technical"],
            "years_of_experience": 7.5,
            "past_project_types": ["Mobile"],
            "certifications": ["iOS Developer", "Android Developer"],
            "education": "B.S. Software Engineering",
            "availability_percent": 80.0,
            "performance_score": 9.0,
            "languages": ["Swift", "Kotlin", "Dart", "JavaScript"],
            "frameworks": ["React Native", "Flutter", "SwiftUI"],
            "domain_expertise": ["Mobile Banking", "Healthcare Apps"]
        },
        {
            "employee_id": "EMP005",
            "name": "Jessica Williams",
            "email": "jessica.williams@company.com",
            "department": "QA & Automation",
            "location": "Chicago",
            "designation": "Senior Automation Engineer",
            "skills": ["Automation", "RPA", "Python", "Selenium", "Test Automation"],
            "skill_proficiency": [5, 4, 4, 4, 4],
            "skill_types": ["Technical", "Technical", "Technical", "Technical", "Technical"],
            "years_of_experience": 5.5,
            "past_project_types": ["Automation"],
            "certifications": ["Selenium Professional", "RPA Certified"],
            "education": "B.S. Information Systems",
            "availability_percent": 95.0,
            "performance_score": 8.5,
            "languages": ["Python", "Java"],
            "frameworks": ["Selenium", "Robot Framework", "Pytest"],
            "domain_expertise": ["Enterprise Automation", "Testing"]
        },
        {
            "employee_id": "EMP006",
            "name": "Robert Taylor",
            "email": "robert.taylor@company.com",
            "department": "Enterprise Solutions",
            "location": "Boston",
            "designation": "ERP Solutions Architect",
            "skills": ["ERP Systems", "SAP", "Oracle", "PostgreSQL", "Integration"],
            "skill_proficiency": [5, 5, 4, 4, 5],
            "skill_types": ["Technical", "Technical", "Technical", "Technical", "Technical"],
            "years_of_experience": 12.0,
            "past_project_types": ["ERP"],
            "certifications": ["SAP Certified", "Oracle Certified Professional"],
            "education": "M.B.A. Information Systems",
            "availability_percent": 75.0,
            "performance_score": 9.3,
            "languages": ["ABAP", "SQL", "Java"],
            "frameworks": ["SAP Fiori", "Oracle Fusion"],
            "domain_expertise": ["Manufacturing", "Supply Chain"]
        },
        {
            "employee_id": "EMP007",
            "name": "Amanda Brown",
            "email": "amanda.brown@company.com",
            "department": "Engineering",
            "location": "Denver",
            "designation": "Full Stack Developer",
            "skills": ["Python", "Django", "React", "PostgreSQL", "AWS", "Docker"],
            "skill_proficiency": [5, 5, 4, 4, 4, 4],
            "skill_types": ["Technical", "Technical", "Technical", "Technical", "Technical", "Technical"],
            "years_of_experience": 6.5,
            "past_project_types": ["Web"],
            "certifications": ["AWS Certified Developer"],
            "education": "B.S. Computer Science",
            "availability_percent": 88.0,
            "performance_score": 8.7,
            "languages": ["Python", "JavaScript", "TypeScript"],
            "frameworks": ["Django", "React", "Express"],
            "domain_expertise": ["SaaS", "EdTech"]
        },
        {
            "employee_id": "EMP008",
            "name": "James Wilson",
            "email": "james.wilson@company.com",
            "department": "Data Science",
            "location": "San Francisco",
            "designation": "Senior ML Engineer",
            "skills": ["Deep Learning", "PyTorch", "Python", "Data Analysis", "Machine Learning"],
            "skill_proficiency": [5, 5, 5, 4, 5],
            "skill_types": ["Technical", "Technical", "Technical", "Technical", "Technical"],
            "years_of_experience": 9.0,
            "past_project_types": ["AI"],
            "certifications": ["PyTorch Certified", "Deep Learning Specialization"],
            "education": "Ph.D. Computer Science",
            "availability_percent": 65.0,
            "performance_score": 9.4,
            "languages": ["Python", "C++"],
            "frameworks": ["PyTorch", "TensorFlow", "Keras"],
            "domain_expertise": ["Computer Vision", "NLP"]
        },
        {
            "employee_id": "EMP009",
            "name": "Lisa Anderson",
            "email": "lisa.anderson@company.com",
            "department": "Design",
            "location": "Los Angeles",
            "designation": "Senior UI/UX Designer",
            "skills": ["UI/UX Design", "Figma", "Adobe XD", "Web Design", "React"],
            "skill_proficiency": [5, 5, 4, 5, 3],
            "skill_types": ["Design", "Design", "Design", "Design", "Technical"],
            "years_of_experience": 5.0,
            "past_project_types": ["Web", "Mobile"],
            "certifications": ["UI/UX Design Certificate", "Figma Professional"],
            "education": "B.F.A. Graphic Design",
            "availability_percent": 92.0,
            "performance_score": 8.6,
            "languages": ["HTML/CSS", "JavaScript"],
            "frameworks": ["React", "Framer"],
            "domain_expertise": ["Consumer Apps", "E-commerce"]
        },
        {
            "employee_id": "EMP010",
            "name": "Christopher Martinez",
            "email": "christopher.martinez@company.com",
            "department": "Engineering",
            "location": "Miami",
            "designation": "Senior Full Stack Developer",
            "skills": ["JavaScript", "Node.js", "React", "MongoDB", "AWS", "Docker"],
            "skill_proficiency": [5, 5, 5, 4, 4, 4],
            "skill_types": ["Technical", "Technical", "Technical", "Technical", "Technical", "Technical"],
            "years_of_experience": 7.0,
            "past_project_types": ["Web"],
            "certifications": ["Node.js Professional", "MongoDB Certified"],
            "education": "M.S. Software Engineering",
            "availability_percent": 82.0,
            "performance_score": 8.9,
            "languages": ["JavaScript", "TypeScript", "Python"],
            "frameworks": ["Node.js", "Express", "React", "Next.js"],
            "domain_expertise": ["Real-time Systems", "API Development"]
        },
        {
            "employee_id": "EMP011",
            "name": "Maria Garcia",
            "email": "maria.garcia@company.com",
            "department": "Data Science",
            "location": "Austin",
            "designation": "Data Engineer",
            "skills": ["Python", "FastAPI", "PostgreSQL", "Data Analysis", "Pandas", "NumPy"],
            "skill_proficiency": [5, 4, 4, 5, 5, 4],
            "skill_types": ["Technical", "Technical", "Technical", "Technical", "Technical", "Technical"],
            "years_of_experience": 6.0,
            "past_project_types": ["Web", "AI"],
            "certifications": ["Data Engineering Certificate"],
            "education": "M.S. Data Science",
            "availability_percent": 87.0,
            "performance_score": 8.8,
            "languages": ["Python", "SQL", "R"],
            "frameworks": ["FastAPI", "Pandas", "NumPy", "Spark"],
            "domain_expertise": ["Data Analytics", "Business Intelligence"]
        },
        {
            "employee_id": "EMP012",
            "name": "Daniel Lee",
            "email": "daniel.lee@company.com",
            "department": "Engineering",
            "location": "Seattle",
            "designation": "Mobile Development Lead",
            "skills": ["Mobile Development", "iOS", "Swift", "React Native", "PostgreSQL"],
            "skill_proficiency": [5, 5, 5, 4, 3],
            "skill_types": ["Technical", "Technical", "Technical", "Technical", "Technical"],
            "years_of_experience": 8.0,
            "past_project_types": ["Mobile"],
            "certifications": ["iOS Developer", "React Native Certified"],
            "education": "B.S. Computer Science",
            "availability_percent": 78.0,
            "performance_score": 9.1,
            "languages": ["Swift", "Objective-C", "JavaScript"],
            "frameworks": ["React Native", "SwiftUI", "UIKit"],
            "domain_expertise": ["Mobile Banking", "Healthcare Apps"]
        }
    ]
    
    for emp_data in sample_employees:
        employee = Employee(**emp_data)
        db.add(employee)
    
    db.commit()
    print(f"Created {len(sample_employees)} sample employees")


def main():
    """Main seeding function"""
    print("Initializing database...")
    init_db()
    
    db = SessionLocal()
    try:
        print("Creating sample employees...")
        create_sample_employees(db)
        
        print("Seed data created successfully!")
    except Exception as e:
        print(f"Error seeding data: {e}")
        db.rollback()
    finally:
        db.close()


if __name__ == "__main__":
    main()
