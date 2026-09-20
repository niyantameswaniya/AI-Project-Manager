# AI Project Manager - ML-Powered Project Management System

A sophisticated AI-powered project management application that uses machine learning to predict optimal team size, required skills, and best-fit employees for projects.

## 🎯 Features

### Core Functionality
- **Project Intake Module**: Upload and manage project details with comprehensive metadata
- **Employee Database**: Maintain employee profiles with skills, experience, and availability
- **ML-Powered Predictions**: 
  - Team size prediction using Random Forest Regression
  - Skill requirement classification using Multi-label Classification
  - Intelligent employee matching with similarity scoring
- **Royal Premium UI**: Dark theme with gold accents, glassmorphism effects, and elegant typography
- **Analytics Dashboard**: Comprehensive insights with charts and visualizations

## 🏗️ Architecture

### Backend (Python/FastAPI)
- **Framework**: FastAPI with SQLAlchemy ORM
- **Database**: PostgreSQL
- **ML Pipeline**: Scikit-learn (Random Forest, TF-IDF Vectorization)
- **Features**:
  - RESTful API endpoints
  - ML model training and inference
  - Employee matching engine with weighted scoring

### Frontend (React)
- **Framework**: React 18 with Vite
- **Styling**: Tailwind CSS with custom royal theme
- **Animations**: Framer Motion
- **Charts**: Recharts
- **Features**:
  - Responsive design
  - Real-time predictions
  - Interactive dashboards

## 📁 Project Structure

```
project_manager/
├── backend/
│   ├── app/
│   │   ├── __init__.py
│   │   ├── main.py              # FastAPI application
│   │   ├── database.py           # Database configuration
│   │   ├── models.py             # SQLAlchemy models
│   │   ├── schemas.py            # Pydantic schemas
│   │   ├── ml/
│   │   │   ├── pipeline.py       # ML training & prediction
│   │   │   └── matching.py       # Employee matching engine
│   │   └── api/
│   │       ├── projects.py       # Project endpoints
│   │       ├── employees.py      # Employee endpoints
│   │       └── predictions.py   # Analytics endpoints
│   ├── requirements.txt
│   ├── seed_data.py             # Database seeding script
│   └── train_models.py          # ML model training script
├── frontend/
│   ├── src/
│   │   ├── components/          # React components
│   │   ├── pages/               # Page components
│   │   ├── services/            # API services
│   │   ├── App.jsx
│   │   └── main.jsx
│   ├── package.json
│   └── tailwind.config.js
└── ml_models/                   # Saved ML models (generated)
```

## 🚀 Setup Instructions

### Prerequisites
- Python 3.9+
- Node.js 18+
- PostgreSQL 12+
- pip and npm

### Backend Setup

1. **Navigate to backend directory**:
```bash
cd backend
```

2. **Create virtual environment**:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. **Install dependencies**:
```bash
pip install -r requirements.txt
```

4. **Configure database**:
   - Create a PostgreSQL database named `project_manager`
   - Update `DATABASE_URL` in `backend/app/database.py` if needed:
   ```python
   DATABASE_URL = "postgresql://username:password@localhost:5432/project_manager"
   ```

5. **Initialize database and seed data**:
```bash
python seed_data.py
```

6. **Train ML models**:
```bash
python train_models.py
```

7. **Start the backend server**:
```bash
uvicorn app.main:app --reload --port 8000
```

The API will be available at `http://localhost:8000`
API documentation: `http://localhost:8000/docs`

### Frontend Setup

1. **Navigate to frontend directory**:
```bash
cd frontend
```

2. **Install dependencies**:
```bash
npm install
```

3. **Start development server**:
```bash
npm run dev
```

The frontend will be available at `http://localhost:3000`

## 📊 Database Schema

### Projects Table
- `id`: Primary key
- `name`: Project name
- `description`: Project description
- `category`: Web/AI/Mobile/Automation/ERP
- `complexity`: Low/Medium/High
- `estimated_timeline_weeks`: Timeline in weeks
- `budget_range`: Optional budget range
- `client_priority`: Low/Medium/High/Critical
- `predicted_team_size`: ML prediction result
- `predicted_skills`: Array of predicted skills
- `confidence_score`: Prediction confidence

### Employees Table
- `id`: Primary key
- `employee_id`: Unique employee identifier
- `name`: Employee name
- `skills`: Array of skill names
- `skill_proficiency`: Array of proficiency levels (1-5)
- `years_of_experience`: Years of experience
- `past_project_types`: Array of past project categories
- `availability_percent`: Availability percentage
- `performance_score`: Performance score (1-10)

## 🤖 ML Pipeline

### Models

1. **Team Size Regression Model**
   - Algorithm: Random Forest Regressor
   - Features: Project description (TF-IDF), category, complexity, priority, timeline
   - Output: Predicted team size (integer)

2. **Skill Classification Model**
   - Algorithm: Random Forest Classifier (Multi-label)
   - Features: Same as team size model
   - Output: Required skills with confidence scores

3. **Employee Matching Engine**
   - Algorithm: Weighted scoring with similarity matching
   - Factors:
     - Skill match (40%)
     - Experience relevance (25%)
     - Availability (20%)
     - Performance (15%)
   - Output: Ranked employee recommendations with match scores

### Training Data

The system uses historical project data to train models. Sample projects are included in `seed_data.py`. In production, you would use actual historical project data with known team sizes and required skills.

## 🎨 UI/UX Features

- **Royal Theme**: Dark navy background (#0a1628) with gold accents (#d4af37)
- **Glassmorphism**: Frosted glass effect cards with backdrop blur
- **Typography**: Playfair Display for headings, Poppins for body text
- **Animations**: Smooth transitions and hover effects using Framer Motion
- **Responsive Design**: Mobile-first approach with Tailwind CSS

## 📡 API Endpoints

### Projects
- `GET /api/projects` - Get all projects
- `GET /api/projects/{id}` - Get project by ID
- `POST /api/projects` - Create new project
- `POST /api/projects/{id}/predict` - Generate ML predictions

### Employees
- `GET /api/employees` - Get all employees
- `GET /api/employees/{id}` - Get employee by ID
- `POST /api/employees` - Create new employee

### Analytics
- `GET /api/analytics` - Get analytics and insights

## 🔧 Configuration

### Environment Variables

Create a `.env` file in the backend directory (optional):
```
DATABASE_URL=postgresql://user:password@localhost:5432/project_manager
```

### Model Training

Models are automatically loaded on API startup. To retrain:
```bash
python train_models.py
```

Trained models are saved in `ml_models/` directory.

## 🧪 Testing

### Backend API Testing
Use the interactive API docs at `http://localhost:8000/docs` or use curl:

```bash
# Create a project
curl -X POST "http://localhost:8000/api/projects" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Test Project",
    "description": "A test project description",
    "category": "Web",
    "complexity": "Medium",
    "estimated_timeline_weeks": 8,
    "client_priority": "High"
  }'

# Generate predictions
curl -X POST "http://localhost:8000/api/projects/1/predict"
```

## 🚀 Deployment

### Backend
1. Set production database URL
2. Run migrations: `python seed_data.py`
3. Train models: `python train_models.py`
4. Deploy with gunicorn: `gunicorn app.main:app -w 4 -k uvicorn.workers.UvicornWorker`

### Frontend
1. Build: `npm run build`
2. Serve static files from `dist/` directory

## 📝 Notes

- The ML models use simplified training data. For production, use actual historical project data.
- Employee matching considers skill similarity, not exact matches.
- Confidence scores are calculated based on model predictions and may vary.
- The system is designed to be extensible - add more features as needed.

## 🎯 Future Enhancements

- Auto-retrain ML models with new project data
- AI explainability panel for predictions
- Admin override for employee suggestions
- Skill heatmaps and visualizations
- Real-time collaboration features
- Integration with external HR systems

## 📄 License

This project is provided as-is for educational and development purposes.

## 👥 Contributing

Contributions are welcome! Please feel free to submit issues or pull requests.

---

**Built with ❤️ using FastAPI, React, and Scikit-learn**


