"""FastAPI main application"""
from pathlib import Path

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse

from .database import init_db
from .api import projects, employees, predictions

app = FastAPI(
    title="AI Project Manager",
    description="ML-powered project management system with intelligent employee matching",
    version="1.0.0"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "http://localhost:5173",
        "http://127.0.0.1:3000",
        "http://127.0.0.1:5173",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include API routers
app.include_router(projects.router)
app.include_router(employees.router)
app.include_router(predictions.router)

# Serve frontend build (when running single server)
FRONTEND_DIST = Path(__file__).resolve().parent.parent.parent / "frontend" / "dist"
if FRONTEND_DIST.exists():
    app.mount("/assets", StaticFiles(directory=FRONTEND_DIST / "assets"), name="assets")


@app.on_event("startup")
async def startup_event():
    """Initialize database on startup"""
    init_db()
    print("Database initialized")


@app.get("/health")
def health_check():
    """Health check endpoint"""
    return {"status": "healthy"}


# Serve frontend SPA - only specific paths so /api/* is not caught
if FRONTEND_DIST.exists():
    def _serve_index():
        index_path = FRONTEND_DIST / "index.html"
        if index_path.exists():
            return FileResponse(index_path)
        raise HTTPException(status_code=404, detail="Not found")

    @app.get("/")
    def root():
        return _serve_index()

    # SPA routes - return index.html so client-side router works (do NOT catch /api/*)
    @app.get("/upload")
    def spa_upload():
        return _serve_index()

    @app.get("/employees")
    def spa_employees():
        return _serve_index()

    @app.get("/employees/upload")
    def spa_employees_upload():
        return _serve_index()

    @app.get("/analytics")
    def spa_analytics():
        return _serve_index()

    @app.get("/my-projects")
    def spa_my_projects():
        return _serve_index()

    @app.get("/project/{path:path}")
    def spa_project(path: str):
        return _serve_index()
else:
    @app.get("/")
    def root():
        """Root endpoint when frontend not built"""
        return {
            "message": "AI Project Manager API",
            "version": "1.0.0",
            "docs": "/docs",
            "hint": "To serve the app: cd frontend && npm run build, then restart backend"
        }


