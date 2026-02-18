# HRMS Lite

A lightweight Human Resource Management System (HRMS) built with React (Vite) and Python (FastAPI).

## Overview
HRMS Lite allows an admin to:
- Manage employee records (Add, List, Delete).
- Track daily attendance (Mark Present/Absent).
- View attendance history.

## Tech Stack
- **Frontend**: React, Vite, Tailwind CSS, Axios, React Router.
- **Backend**: Python, FastAPI, Motor (Async MongoDB), Pydantic.
- **Database**: MongoDB Atlas.

## Prerequisites
- Node.js (v14+)
- Python (v3.8+)
- MongoDB Atlas (Running locally or cloud URI)

## Setup Instructions

### 1. Backend Setup
1. Navigate to the `backend` directory:
   ```sh
   cd backend
   ```
2. Create and activate a virtual environment:
   ```sh
   python -m venv venv
   # Windows:
   venv\Scripts\activate
   # Mac/Linux:
   source venv/bin/activate
   ```
3. Install dependencies:
   ```sh
   pip install -r requirements.txt
   ```
4. Create a `.env` file (if not exists) with your MongoDB URI:
   ```
   MONGO_URI=mongodb+srv://<username>:<password>@hrms-lite.0zjzj.mongodb.net/hrms_lite
   DB_NAME=hrms_lite
   ```
5. Start the server:
   ```sh
   uvicorn main:app --reload
   ```
   The API will run at `http://localhost:8000`.

### 2. Frontend Setup
1. Navigate to the `frontend` directory:
   ```sh
   cd frontend
   ```
2. Install dependencies:
   ```sh
   npm install
   ```
3. Start the development server:
   ```sh
   npm run dev
   ```
   The application will run at `http://localhost:5173`.

## Deployment
- **Frontend**: deployed to Vercel platforms.
- **Backend**:deployed to Render.
- **Database**: Using MongoDB Atlas for a cloud database.

## API Endpoints
- `GET /api/employees`: List employees
- `POST /api/employees`: Add employee
- `DELETE /api/employees/{id}`: Delete employee
- `POST /api/attendance`: Mark attendance
- `GET /api/attendance/{id}`: Get attendance records
