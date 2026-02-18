from fastapi import APIRouter, HTTPException, status
from fastapi.responses import JSONResponse
from typing import List
from models import AttendanceModel
from database import get_database
from fastapi.encoders import jsonable_encoder
import traceback

router = APIRouter()

@router.post("/", response_description="Mark attendance")
async def mark_attendance(attendance: AttendanceModel):
    db = get_database()
    attendance_dict = jsonable_encoder(attendance)
    
    if attendance_dict.get("_id") is None:
        attendance_dict.pop("_id", None)
    
    # Verify employee exists
    emp = await db["employees"].find_one({"employee_id": attendance_dict["employee_id"]})
    if not emp:
        raise HTTPException(status_code=404, detail="Employee not found")

    # Check if attendance already marked for this date
    existing_record = await db["attendance"].find_one({
        "employee_id": attendance_dict["employee_id"],
        "date": attendance_dict["date"]
    })
    
    if existing_record:
        raise HTTPException(status_code=400, detail="Attendance already marked for this date")

    new_attendance = await db["attendance"].insert_one(attendance_dict)
    created_attendance = await db["attendance"].find_one({"_id": new_attendance.inserted_id})
    # Convert ObjectId to string for JSON serialization
    if created_attendance:
        created_attendance["_id"] = str(created_attendance["_id"])
    return created_attendance

@router.get("/{employee_id}", response_description="Get attendance records for an employee")
async def get_attendance(employee_id: str):
    db = get_database()
    attendance_records = await db["attendance"].find({"employee_id": employee_id}).to_list(1000)
    # Convert ObjectId to string for JSON serialization
    for record in attendance_records:
        record["_id"] = str(record["_id"])
    return attendance_records
