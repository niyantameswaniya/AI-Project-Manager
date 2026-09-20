# Quick Setup Guide

## Prerequisites Check

Before starting, ensure you have:
- ✅ Python 3.9+ installed
- ✅ Node.js 18+ installed
- ✅ PostgreSQL 12+ installed and running
- ✅ pip and npm available in terminal

## Step-by-Step Setup

### 1. Database Setup

```bash
# Create PostgreSQL database
createdb project_manager

# Or using psql:
psql -U postgres
CREATE DATABASE project_manager;
\q
```

### 2. Backend Setup

```bash
# Navigate to backend
cd backend

# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Update database URL in app/database.py if needed
# Default: postgresql://postgres:postgres@localhost:5432/project_manager

# Seed database with sample data
python seed_data.py

# Train ML models
python train_models.py

# Start backend server
uvicorn app.main:app --reload --port 8000
```

Backend should now be running at `http://localhost:8000`

### 3. Frontend Setup

Open a new terminal window:

```bash
# Navigate to frontend
cd frontend

# Install dependencies
npm install

# Start development server
npm run dev
```

Frontend should now be running at `http://localhost:3000`

## Verify Installation

1. **Backend**: Visit `http://localhost:8000/docs` - You should see FastAPI documentation
2. **Frontend**: Visit `http://localhost:3000` - You should see the Royal Dashboard

## First Steps

1. **View Dashboard**: Navigate to `http://localhost:3000`
2. **Upload Project**: Click "Upload Project" and fill in project details
3. **Generate Predictions**: On the project details page, click "Generate Predictions"
4. **View Analytics**: Check the Analytics page for insights
5. **Browse Employees**: View the employee database

## Troubleshooting

### Database Connection Error
- Ensure PostgreSQL is running
- Check database credentials in `backend/app/database.py`
- Verify database exists: `psql -U postgres -l`

### ML Models Not Found
- Run `python backend/train_models.py` to generate models
- Check that `ml_models/` directory exists

### Frontend Not Connecting to Backend
- Verify backend is running on port 8000
- Check `frontend/vite.config.js` proxy settings
- Ensure CORS is enabled in backend (already configured)

### Port Already in Use
- Backend: Change port in uvicorn command: `--port 8001`
- Frontend: Update `vite.config.js` server.port

## Next Steps

- Add more employees to the database
- Create more projects to improve ML predictions
- Customize the UI theme in `frontend/tailwind.config.js`
- Extend ML models with more features

## Production Deployment

For production deployment:
1. Set proper environment variables
2. Use production database
3. Build frontend: `npm run build`
4. Use production WSGI server (gunicorn)
5. Configure reverse proxy (nginx)

See README.md for more details.


