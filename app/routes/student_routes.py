from fastapi import APIRouter
from bson import ObjectId
from app.database.connection import (
    students_collection,
    users_collection,
)
from app.schemas.students_schema import (
    StudentCreate,
    StudentUpdate
)
from fastapi import HTTPException

router = APIRouter(
    prefix="/students",
    tags=["Students"]
)

@router.post("/")
def create_student(student: StudentCreate):
    existing_user = users_collection.find_one(
        {"email": student.email}
    )

    if existing_user:
        raise HTTPException(
            status_code=400,
            detail="Email already exists"
        )

    student_data = {
    "name": student.name,
    "email": student.email,
    "class_name": student.class_name,
    "gender": student.gender,
    "phone": student.phone,
    "address": student.address,
    "parent_name": student.parent_name,
    "status": "Active"
}
    students_collection.insert_one(student_data)

    user_data = {
        "name": student.name,
        "email": student.email,
        "password": student.password,
        "role": "student"
    }

    users_collection.insert_one(user_data)

    return {
        "message": "Student Created Successfully"
    }

@router.get("/")
def get_students():

    students = list(
        students_collection.find({})
    )

    for student in students:
        student["_id"] = str(student["_id"])

    return students
@router.get("/{student_id}")
def get_student(student_id: str):

    student = students_collection.find_one(
        {"_id": ObjectId(student_id)}
    )

    if not student:
        raise HTTPException(
            status_code=404,
            detail="Student Not Found"
        )

    student["_id"] = str(student["_id"])

    return student

@router.put("/{student_id}")
def update_student(
    student_id: str,
    student: StudentUpdate
):

    result = students_collection.update_one(
        {"_id": ObjectId(student_id)},
        {
            "$set": {
                "name": student.name,
                "email": student.email,
                "class_name": student.class_name,
                "gender": student.gender,
                "phone": student.phone,
                "address": student.address,
                "parent_name": student.parent_name,
                "status": student.status,
        }
        }
    )

    users_collection.update_one(
        {"email": student.email},
        {
            "$set": {
                "name": student.name
            }
        }
    )

    if result.modified_count == 0:
        return {
            "message": "No changes made"
        }

    return {
        "message": "Student Updated Successfully"
    }

@router.delete("/{student_id}")
def delete_student(student_id: str):

    student = students_collection.find_one(
        {"_id": ObjectId(student_id)}
    )

    if not student:
        return {
            "message": "Student Not Found"
        }

    students_collection.delete_one(
        {"_id": ObjectId(student_id)}
    )

    users_collection.delete_one(
        {"email": student["email"]}
    )

    return {
        "message": "Student Deleted Successfully"
    }