import httpx
import asyncio
import datetime

BASE_URL = "http://localhost:8000/api"

async def test_api():
    async with httpx.AsyncClient() as client:
        # 1. Create Employee
        emp_data = {
            "employee_id": "TEST001",
            "name": "Test User",
            "email": "test@example.com",
            "department": "QA"
        }
        print(f"Creating employee: {emp_data['employee_id']}")
        resp = await client.post(f"{BASE_URL}/employees/", json=emp_data)
        if resp.status_code == 200:
            print("Employee created successfully")
        else:
            print(f"Failed to create employee: {resp.text}")

        # 2. Get Employees
        print("Fetching employees...")
        resp = await client.get(f"{BASE_URL}/employees/")
        employees = resp.json()
        print(f"Found {len(employees)} employees")
        
        # 3. Mark Attendance
        att_data = {
            "employee_id": "TEST001",
            "date": datetime.date.today().isoformat(),
            "status": "Present"
        }
        print(f"Marking attendance for {att_data['employee_id']}")
        resp = await client.post(f"{BASE_URL}/attendance/", json=att_data)
        if resp.status_code == 200:
            print("Attendance marked successfully")
        elif resp.status_code == 400 and "already marked" in resp.text:
             print("Attendance already marked (Expected if re-running)")
        else:
            print(f"Failed to mark attendance: {resp.text}")

        # 4. Get Attendance
        print(f"Fetching attendance for {att_data['employee_id']}")
        resp = await client.get(f"{BASE_URL}/attendance/{att_data['employee_id']}")
        records = resp.json()
        print(f"Found {len(records)} attendance records")

        # 5. Delete Employee
        print(f"Deleting employee: {emp_data['employee_id']}")
        resp = await client.delete(f"{BASE_URL}/employees/TEST001")
        if resp.status_code == 200:
            print("Employee deleted successfully")
        else:
            print(f"Failed to delete employee: {resp.text}")

if __name__ == "__main__":
    asyncio.run(test_api())
