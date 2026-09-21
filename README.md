# AI Project Manager

An AI-based project management system that helps turn a project idea into a structured project with tasks and also helps in selecting suitable employees for the project.

I developed this project as my M.Sc. Artificial Intelligence major project. The main idea was to use AI for some of the parts of project management that normally require manual planning.

## What the project does

The system mainly focuses on two things:

1. Structuring a project from a given project idea.
2. Recommending employees based on their skills and availability.

A user can enter a project idea, and the system can generate a more structured version of the project along with tasks. The employee recommendation part uses semantic similarity to find people whose skills are relevant to the project requirements.

## Main Features

### Project and Task Generation

The project uses the Gemini API to process a project description and convert it into a structured format.

It can help with:

- Project title and description
- Project tasks
- Task details
- Project planning information
- Tracking project progress

### Employee Recommendation

The system also includes an employee recommendation module.

Employee profiles and project requirements are converted into vector representations using a Sentence Transformer model. FAISS is then used for similarity search to find employees whose skills are closer to the requirements.

RapidFuzz is also used where text similarity is useful.

### Project Management

The application provides functionality for managing:

- Projects
- Tasks
- Employees
- Project progress
- Employee assignment

## Technologies Used

### Backend

- Python
- FastAPI
- Gemini API
- Supabase
- JWT Authentication

### Machine Learning

- Sentence Transformers
- FAISS
- RapidFuzz

### Frontend

- JavaScript
- React
- Vite
- Tailwind CSS

## Project Structure

```text
AI-Project-Manager/
│
├── backend/
│   ├── app/
│   ├── ml_models/
│   └── ...
│
├── frontend/
│   ├── src/
│   ├── index.html
│   └── ...
│
├── .gitignore
├── database_schema.sql
├── README.md
└── ...