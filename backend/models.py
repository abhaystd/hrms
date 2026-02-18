from pydantic import BaseModel, Field, EmailStr, ConfigDict, BeforeValidator
from typing import Optional, List, Annotated
from datetime import date

# Pydantic v2 compatible ObjectId
PyObjectId = Annotated[str, BeforeValidator(str)]

class EmployeeModel(BaseModel):
    id: Optional[PyObjectId] = Field(alias="_id", default=None)
    employee_id: str = Field(..., min_length=1, description="Unique Employee ID")
    name: str = Field(..., min_length=1)
    email: EmailStr
    department: str = Field(..., min_length=1)

    model_config = ConfigDict(
        populate_by_name=True,
        arbitrary_types_allowed=True,
        json_schema_extra = {
            "example": {
                "employee_id": "EMP001",
                "name": "Jane Doe",
                "email": "jane@example.com",
                "department": "Engineering"
            }
        }
    )

class AttendanceModel(BaseModel):
    id: Optional[PyObjectId] = Field(alias="_id", default=None)
    employee_id: str = Field(..., description="Employee ID reference")
    date: date
    status: str = Field(..., pattern="^(Present|Absent)$")

    model_config = ConfigDict(
        populate_by_name=True,
        arbitrary_types_allowed=True,
        json_schema_extra = {
            "example": {
                "employee_id": "EMP001",
                "date": "2023-10-27",
                "status": "Present"
            }
        }
    )

