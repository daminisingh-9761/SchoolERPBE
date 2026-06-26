from fastapi import APIRouter

from app.database.connection import (
    students_collection,
    teachers_collection,
    attendance_collection,
    fees_collection,
    fee_payments_collection
)
from datetime import date, timedelta

router = APIRouter(
    prefix="/dashboard",
    tags=["Dashboard"]
)

@router.get("/admin")
def admin_dashboard():

    today = str(date.today())

    total_students = students_collection.count_documents({})

    total_teachers = teachers_collection.count_documents({})

    present_today = attendance_collection.count_documents({
        "date": today,
        "attendance_status": "Present"
    })

    absent_today = attendance_collection.count_documents({
        "date": today,
        "attendance_status": "Absent"
    })
    attendance_rate = 0

    if (present_today + absent_today) > 0:

        attendance_rate = round(
            (present_today /
             (present_today + absent_today)) * 100,
            2
        )
    weekly_attendance = []

    for i in range(6, -1, -1):

        current_day = date.today() - timedelta(days=i)

        current_date = str(current_day)

        present = attendance_collection.count_documents({
            "date": current_date,
            "attendance_status": "Present"
        })

        absent = attendance_collection.count_documents({
            "date": current_date,
            "attendance_status": "Absent"
        })

        weekly_attendance.append({
            "day": current_day.strftime("%a"),
            "present": present,
            "absent": absent
        })
        from collections import defaultdict
        monthly_revenue = defaultdict(int)

        payments = list(
            fee_payments_collection.find({})
        )

        for payment in payments:

            payment_date = payment.get(
                "payment_date"
            )

            if not payment_date:
                continue

            month = payment_date[:7]

            monthly_revenue[month] += payment.get(
                "amount",
                0
            )

        fees_chart = []

        for month in sorted(monthly_revenue.keys()):

            fees_chart.append({

                "month": month,

                "fees": monthly_revenue[month]

            })

    return {
    "total_students": total_students,
    "total_teachers": total_teachers,
    "present_today": present_today,
    "absent_today": absent_today,
    "attendance_rate": attendance_rate,
    "weekly_attendance": weekly_attendance,
    "fees_chart": fees_chart
}