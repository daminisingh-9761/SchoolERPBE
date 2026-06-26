from fastapi import APIRouter, HTTPException

from app.schemas.auth_schema import LoginRequest

from app.database.connection import (
    users_collection,
    students_collection
)

router = APIRouter(
    prefix="/auth",
    tags=["Authentication"]
)
@router.post("/login")
def login(payload: LoginRequest):

    user = users_collection.find_one(
        {"email": payload.email}
    )

    if not user:
        raise HTTPException(
            status_code=401,
            detail="Invalid Email"
        )

    if user["password"] != payload.password:
        raise HTTPException(
            status_code=401,
            detail="Invalid Password"
        )

    student_id = None

    if user["role"] == "student":

        student = students_collection.find_one(
            {"email": user["email"]}
        )

        if student:
            student_id = str(student["_id"])

    return {
        "message": "Login Successful",
        "role": user["role"],
        "name": user["name"],
        "email": user["email"],
        "student_id": student_id
    }