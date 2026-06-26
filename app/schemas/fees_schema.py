from pydantic import BaseModel

class FeeCreate(BaseModel):
    student_id: str
    student_name: str
    class_name: str
    session: str
    fee_amount: float
    due_date: str

class PaymentCreate(BaseModel):
    payment_amount: int

class FeeUpdate(BaseModel):
    fee_amount: int
    due_date: str