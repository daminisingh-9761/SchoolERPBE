from fastapi import APIRouter
from fastapi import APIRouter, HTTPException
from app.database.connection import (
    teachers_collection,
    users_collection
)
from app.schemas.teachers_schema import TeacherCreate
from bson import ObjectId
from app.schemas.teachers_schema import TeacherUpdate

router = APIRouter(
    prefix="/teachers",
    tags=["Teachers"]
)

# @router.get("/")
# def get_teachers():

#     return {
#         "message": "Teachers API Working"
#     }

@router.post("/")
def create_teacher(teacher: TeacherCreate):

    existing_user = users_collection.find_one(
        {"email": teacher.email}
    )

    if existing_user:
        raise HTTPException(
            status_code=400,
            detail="Email already exists"
        )

    teacher_data = {
        "name": teacher.name,
        "email": teacher.email,
        "subject": teacher.subject,
        "phone": teacher.phone,
        "address": teacher.address,
        "status": "Active"
    }

    teachers_collection.insert_one(
        teacher_data
    )

    user_data = {
        "name": teacher.name,
        "email": teacher.email,
        "password": teacher.password,
        "role": "teacher"
    }

    users_collection.insert_one(
        user_data
    )

    return {
        "message": "Teacher Created Successfully"
    }

@router.get("/")
def get_teachers():

    teachers = list(
        teachers_collection.find({})
    )

    for teacher in teachers:
        teacher["_id"] = str(teacher["_id"])

    return teachers
  
@router.put("/{teacher_id}")
def update_teacher(
    teacher_id: str,
    teacher: TeacherUpdate
):

    result = teachers_collection.update_one(
        {"_id": ObjectId(teacher_id)},
        {
            "$set": {
                "name": teacher.name,
                "email": teacher.email,
                "subject": teacher.subject,
                "phone": teacher.phone,
                "address": teacher.address,
                "status": teacher.status
            }
        }
    )

    users_collection.update_one(
        {"email": teacher.email},
        {
            "$set": {
                "name": teacher.name
            }
        }
    )

    if result.modified_count == 0:
        return {
            "message": "No changes made"
        }

    return {
        "message": "Teacher Updated Successfully"
    }

@router.delete("/{teacher_id}")
def delete_teacher(teacher_id: str):

    teacher = teachers_collection.find_one(
        {"_id": ObjectId(teacher_id)}
    )

    if not teacher:
        return {
            "message": "Teacher Not Found"
        }

    teachers_collection.delete_one(
        {"_id": ObjectId(teacher_id)}
    )

    users_collection.delete_one(
        {"email": teacher["email"]}
    )

    return {
        "message": "Teacher Deleted Successfully"
    }