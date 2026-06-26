from pydantic import BaseModel, EmailStr, Field

class StudentCreate(BaseModel):
    name: str = Field(..., min_length=2)
    email: EmailStr
    password: str = Field(..., min_length=6)
    class_name: str = Field(..., min_length=1)
    gender:str
    phone: str = Field(..., min_length=10, max_length=10)
    address: str = Field(..., min_length=3)
    parent_name: str = Field(..., min_length=2)

class StudentUpdate(BaseModel):
    name: str
    email: str
    class_name: str
    gender: str
    phone: str
    address: str
    parent_name: str
    status: str