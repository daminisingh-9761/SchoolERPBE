from fastapi import APIRouter
from datetime import date
from typing import List

from app.database.connection import attendance_collection
from app.schemas.attendance_schemas import AttendanceCreate

router = APIRouter(
    prefix="/attendance",
    tags=["Attendance"]
)

@router.post("/")
def mark_attendance(
    attendance: List[AttendanceCreate]
):

    for record in attendance:

        attendance_data = {
    "student_id": record.student_id,
    "student_name": record.student_name,
    "class_name": record.class_name,
    "attendance_status": record.attendance_status,
    "date": str(date.today())
}
        attendance_collection.update_one(
            {
                "student_id": record.student_id,
                "date": record.date
            },
            {
                "$set": attendance_data
            },
            upsert=True
        )

    return {
        "message": "Attendance Saved Successfully"
    }
@router.get("/")
def get_attendance():

    attendance = list(
        attendance_collection.find({})
    )

    for record in attendance:
        record["_id"] = str(record["_id"])

    return attendance

# from fastapi import APIRouter, Request

# @router.post("/")
# async def mark_attendance(request: Request):
#     body = await request.json()
#     print(body)

#     return {"message": "received"}
from fastapi import Query

@router.get("/by-date")
def get_attendance_by_date(date: str = Query(...)):

    attendance = list(
        attendance_collection.find({
            "date": date
        })
    )

    for record in attendance:
        record["_id"] = str(record["_id"])

    return attendance

@router.get("/student/{student_id}")
def get_student_attendance(student_id: str):

    attendance = list(
        attendance_collection.find(
            {"student_id": student_id}
        )
    )

    for record in attendance:
        record["_id"] = str(record["_id"])

    return attendance

@router.get("/student/{student_id}/summary")
def get_attendance_summary(student_id: str):

    attendance = list(
        attendance_collection.find(
            {"student_id": student_id}
        )
    )

    total_days = len(attendance)

    present_days = len([
        record
        for record in attendance
        if record["attendance_status"] == "Present"
    ])

    absent_days = total_days - present_days

    percentage = 0

    if total_days > 0:
        percentage = round(
            (present_days / total_days) * 100,
            2
        )

    return {
        "total_days": total_days,
        "present_days": present_days,
        "absent_days": absent_days,
        "attendance_percentage": percentage
    }