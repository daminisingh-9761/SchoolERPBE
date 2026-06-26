from fastapi import APIRouter
from app.database.connection import fees_collection
from app.schemas.fees_schema import FeeCreate
from app.schemas.fees_schema import FeeUpdate
from bson import ObjectId
from app.schemas.fees_schema import PaymentCreate
from datetime import date
from datetime import datetime
from app.database.connection import fee_payments_collection
router = APIRouter(
    prefix="/fees",
    tags=["Fees"]
)

@router.post("/")
def assign_fee(fee: FeeCreate):

    existing_fee = fees_collection.find_one({
    "student_id": fee.student_id,
    "session": fee.session
})

    if existing_fee:

        fees_collection.update_one(
    {
        "student_id": fee.student_id,
        "session": fee.session
    },
            {
                "$set": {
                    "session": fee.session,
                    "fee_amount": fee.fee_amount,
                    "remaining_amount": fee.fee_amount,
                    "due_date": fee.due_date
                }
            }
        )

        return {
            "message": "Fee Updated Successfully"
        }

    fees_collection.insert_one({
        "student_id": fee.student_id,
        "student_name": fee.student_name,
        "class_name": fee.class_name,
        "session": fee.session,

        "fee_amount": fee.fee_amount,

        "paid_amount": 0,

        "remaining_amount": fee.fee_amount,

        "status": "Pending",

        "due_date": fee.due_date
    })

    return {
        "message": "Fee Assigned Successfully"
    }
@router.get("/")
def get_fees():

    fees = list(
        fees_collection.find({})
    )

    for fee in fees:
        fee["_id"] = str(fee["_id"])
    
    today = date.today()

    for fee in fees:

        fee["_id"] = str(fee["_id"])

        due_date = datetime.strptime(
            fee["due_date"],
            "%Y-%m-%d"
        ).date()

        if (
            fee["remaining_amount"] > 0
            and due_date < today
        ):
            fee["status"] = "Overdue"

    return fees

@router.put("/payment/{fee_id}")
def collect_payment(
    fee_id: str,
    payment: PaymentCreate
):
    print("step 1")
    fee = fees_collection.find_one(
        {"_id": ObjectId(fee_id)}
    )

    if not fee:
        return {
            "message": "Fee record not found"
        }

    new_paid_amount = (
        fee["paid_amount"] +
        payment.payment_amount
    )

    new_remaining_amount = (
        fee["fee_amount"] -
        new_paid_amount
    )

    new_status = (
        "Paid"
        if new_remaining_amount <= 0
        else "Pending"
    )
    
    print("STEP 2")
    fee_payments_collection.insert_one({
    "fee_id": fee_id,
    "student_id": fee["student_id"],
    "student_name": fee["student_name"],
    "amount": payment.payment_amount,
    "payment_date": str(date.today())
}) 
    
    print("STEP 3")

    fees_collection.update_one(
        {"_id": ObjectId(fee_id)},
        {
            "$set": {
                "paid_amount": new_paid_amount,
                "remaining_amount": new_remaining_amount,
                "status": new_status
            }
        }
    )

    return {
        "message": "Payment Collected Successfully"
    }
@router.put("/{fee_id}")
def update_fee(
    fee_id: str,
   fee: FeeUpdate
):

    existing_fee = fees_collection.find_one(
        {"_id": ObjectId(fee_id)}
    )

    if not existing_fee:
        return {
            "message": "Fee record not found"
        }

    remaining = (
        fee.fee_amount -
        existing_fee["paid_amount"]
    )

    status = (
        "Paid"
        if remaining <= 0
        else "Pending"
    )

    fees_collection.update_one(
        {"_id": ObjectId(fee_id)},
        {
            "$set": {
                "fee_amount": fee.fee_amount,
                "remaining_amount": remaining,
                "due_date": fee.due_date,
                "status": status
            }
        }
    )

    return {
        "message": "Fee Updated Successfully"
    }
@router.delete("/{fee_id}")
def delete_fee(fee_id: str):

    fee = fees_collection.find_one(
        {"_id": ObjectId(fee_id)}
    )

    if not fee:
        return {
            "message": "Fee not found"
        }

    fees_collection.delete_one(
        {"_id": ObjectId(fee_id)}
    )

    fee_payments_collection.delete_many(
        {
            "fee_id": fee_id
        }
    )

    return {
        "message": "Fee Deleted Successfully"
    }

@router.get("/history/{student_id}")
def get_payment_history(
    student_id: str
):
    payments = list(
        fee_payments_collection.find(
            {
                "student_id": student_id
            }
        )
    )

    for payment in payments:
        payment["_id"] = str(
            payment["_id"]
        )

    return payments