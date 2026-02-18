import asyncio
import os
from datetime import date, timedelta
from motor.motor_asyncio import AsyncIOMotorClient
from dotenv import load_dotenv

load_dotenv()

MONGO_URI = os.getenv("MONGO_URI")
DB_NAME = os.getenv("DB_NAME")

async def seed_data():
    client = AsyncIOMotorClient(MONGO_URI)
    db = client[DB_NAME]
    
    # 清空现有数据 (Optional - keep for fresh start)
    # await db["employees"].delete_many({})
    # await db["attendance"].delete_many({})
    
    print("Seeding mock employees...")
    mock_employees = [
        {"employee_id": "EMP001", "name": "John Doe", "email": "john@example.com", "department": "Engineering"},
        {"employee_id": "EMP002", "name": "Jane Smith", "email": "jane@example.com", "department": "Product"},
        {"employee_id": "EMP003", "name": "Alice Johnson", "email": "alice@example.com", "department": "Design"},
        {"employee_id": "EMP004", "name": "Bob Brown", "email": "bob@example.com", "department": "Marketing"},
        {"employee_id": "EMP005", "name": "Charlie Wilson", "email": "charlie@example.com", "department": "HR"},
    ]
    
    for emp in mock_employees:
        if not await db["employees"].find_one({"employee_id": emp["employee_id"]}):
            await db["employees"].insert_one(emp)
            print(f"Added employee: {emp['name']}")
    
    print("\nSeeding attendance records...")
    today = date.today()
    yesterday = today - timedelta(days=1)
    
    attendance_data = []
    # John Doe - Present today, Absent yesterday
    attendance_data.append({"employee_id": "EMP001", "date": str(today), "status": "Present"})
    attendance_data.append({"employee_id": "EMP001", "date": str(yesterday), "status": "Absent"})
    
    # Jane Smith - Present today, Present yesterday
    attendance_data.append({"employee_id": "EMP002", "date": str(today), "status": "Present"})
    attendance_data.append({"employee_id": "EMP002", "date": str(yesterday), "status": "Present"})
    
    # Alice Johnson - Absent today
    attendance_data.append({"employee_id": "EMP003", "date": str(today), "status": "Absent"})
    
    for record in attendance_data:
        if not await db["attendance"].find_one({"employee_id": record["employee_id"], "date": record["date"]}):
            await db["attendance"].insert_one(record)
            print(f"Added attendance for {record['employee_id']} on {record['date']}: {record['status']}")

    client.close()
    print("\nSeeding complete!")

if __name__ == "__main__":
    asyncio.run(seed_data())
