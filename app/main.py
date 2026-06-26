from fastapi import FastAPI

from app.database.connection import db
from app.routes.student_routes import router as student_router
from app.routes.auth_routes import router as auth_router
from app.routes.teachers_routes import router as teacher_router
from fastapi.middleware.cors import CORSMiddleware
from app.routes.attendance_routes import router as attendance_router
from app.routes.fees_routes import router as fees_router
from app.routes.dashboard_routes import router as dashboard_router

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(student_router)
app.include_router(auth_router)
app.include_router(teacher_router)
app.include_router(attendance_router)
app.include_router(fees_router)
app.include_router(dashboard_router)

@app.get("/")
def home():
    return {
        "message": "School ERP Backend Running"
    }