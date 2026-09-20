-- AI Project Manager Database Schema
-- PostgreSQL Database Schema

-- Projects Table
CREATE TABLE IF NOT EXISTS projects (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    description TEXT NOT NULL,
    category VARCHAR(50) NOT NULL CHECK (category IN ('Web', 'AI', 'Mobile', 'Automation', 'ERP')),
    complexity VARCHAR(50) NOT NULL CHECK (complexity IN ('Low', 'Medium', 'High')),
    estimated_timeline_weeks INTEGER NOT NULL,
    budget_range VARCHAR(100),
    client_priority VARCHAR(50) NOT NULL CHECK (client_priority IN ('Low', 'Medium', 'High', 'Critical')),
    predicted_team_size INTEGER,
    predicted_skills TEXT[],
    confidence_score FLOAT,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE
);

CREATE INDEX IF NOT EXISTS idx_projects_name ON projects(name);
CREATE INDEX IF NOT EXISTS idx_projects_category ON projects(category);

-- Employees Table
CREATE TABLE IF NOT EXISTS employees (
    id SERIAL PRIMARY KEY,
    employee_id VARCHAR(50) UNIQUE NOT NULL,
    name VARCHAR(255) NOT NULL,
    skills TEXT[] NOT NULL,
    skill_proficiency INTEGER[] NOT NULL,
    years_of_experience FLOAT NOT NULL,
    past_project_types TEXT[],
    availability_percent FLOAT NOT NULL DEFAULT 100.0,
    performance_score FLOAT NOT NULL DEFAULT 5.0,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX IF NOT EXISTS idx_employees_employee_id ON employees(employee_id);

-- Employee Assignments Table (for tracking project assignments)
CREATE TABLE IF NOT EXISTS employee_assignments (
    id SERIAL PRIMARY KEY,
    project_id INTEGER NOT NULL REFERENCES projects(id) ON DELETE CASCADE,
    employee_id INTEGER NOT NULL REFERENCES employees(id) ON DELETE CASCADE,
    match_score FLOAT NOT NULL,
    match_reason TEXT,
    assigned_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX IF NOT EXISTS idx_assignments_project ON employee_assignments(project_id);
CREATE INDEX IF NOT EXISTS idx_assignments_employee ON employee_assignments(employee_id);

-- ML Models Metadata Table
CREATE TABLE IF NOT EXISTS ml_models (
    id SERIAL PRIMARY KEY,
    model_name VARCHAR(100) NOT NULL,
    model_type VARCHAR(50) NOT NULL,
    model_path VARCHAR(255) NOT NULL,
    accuracy FLOAT,
    trained_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    version VARCHAR(20) NOT NULL DEFAULT '1.0'
);

-- Comments
COMMENT ON TABLE projects IS 'Stores project information and ML predictions';
COMMENT ON TABLE employees IS 'Stores employee profiles with skills and experience';
COMMENT ON TABLE employee_assignments IS 'Tracks employee-project assignments with match scores';
COMMENT ON TABLE ml_models IS 'Metadata for trained ML models';


