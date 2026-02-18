from fastapi import APIRouter, HTTPException, status
from typing import List
from models import EmployeeModel
from database import get_database
from fastapi.encoders import jsonable_encoder

router = APIRouter()


@router.post("/", response_description="Add new employee", response_model=EmployeeModel)
async def create_employee(employee: EmployeeModel):
    db = get_database()
    employee_dict = jsonable_encoder(employee)
    if employee_dict.get("_id") is None:
        employee_dict.pop("_id", None)
    # Check for duplicate employee_id
    if await db["employees"].find_one({"employee_id": employee_dict["employee_id"]}):
         raise HTTPException(status_code=400, detail="Employee ID already exists")
    
    new_employee = await db["employees"].insert_one(employee_dict)
    created_employee = await db["employees"].find_one({"_id": new_employee.inserted_id})
    return created_employee

@router.get("/", response_description="List all employees", response_model=List[EmployeeModel])
async def list_employees():
    db = get_database()
    employees = await db["employees"].find().to_list(1000)
    return employees

@router.delete("/{employee_id}", response_description="Delete an employee")
async def delete_employee(employee_id: str):
    db = get_database()
    delete_result = await db["employees"].delete_one({"employee_id": employee_id})

    if delete_result.deleted_count == 1:
        return {"message": f"Employee {employee_id} deleted successfully"}

    raise HTTPException(status_code=404, detail=f"Employee {employee_id} not found")
