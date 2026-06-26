from pydantic import BaseModel

class AttendanceCreate(BaseModel):
    student_id: str
    student_name: str
    class_name: str
    date: str
    attendance_status: str