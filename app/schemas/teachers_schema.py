from pydantic import BaseModel, EmailStr, Field
from typing import Optional


class TeacherCreate(BaseModel):
    name: str = Field(..., min_length=2)
    email: EmailStr
    password: str = Field(..., min_length=6)
    subject: str = Field(..., min_length=1)
    phone: str = Field(..., min_length=10)
    address: str = Field(..., min_length=3)


class TeacherUpdate(BaseModel):
    name: str
    email: EmailStr
    subject: str
    phone: str
    address: str
    status: str