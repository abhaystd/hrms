from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from database import connect_to_mongo, close_mongo_connection
from routes import employee, attendance
import os
from dotenv import load_dotenv

load_dotenv()

app = FastAPI(title="HRMS Lite API", redirect_slashes=False)

# CORS - allow all origins for development
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Database Connection Events
app.add_event_handler("startup", connect_to_mongo)
app.add_event_handler("shutdown", close_mongo_connection)

# Routes
app.include_router(employee.router, prefix="/api/employees", tags=["Employees"])
app.include_router(attendance.router, prefix="/api/attendance", tags=["Attendance"])

@app.get("/")
async def root():
    return {"message": "Welcome to HRMS Lite API"}

@app.get("/api/health")
async def health_check():
    print("Health check endpoint hit!")
    from database import get_database
    try:
        db = get_database()
        if db is None:
            return {"status": "Unhealthy", "database": "Disconnected", "detail": "Database not initialized"}
        
        await db.command("ping")
        return {
            "status": "Healthy",
            "database": "Connected",
            "environment": os.getenv("DB_NAME", "Unknown")
        }
    except Exception as e:
        print(f"Health check failed: {e}")
        return {
            "status": "Unhealthy",
            "database": f"Error: {str(e)}"
        }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)