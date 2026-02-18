import React, { useEffect, useState } from 'react';
import api from '../services/api';

const Dashboard = () => {
    const [stats, setStats] = useState({
        totalEmployees: 0,
        presentToday: 0
    });
    const [loading, setLoading] = useState(true);

    useEffect(() => {
        const fetchStats = async () => {
            try {
                const employeesRes = await api.get('/employees/');
                // efficient way would be to have a dedicated stats endpoint, 
                // but for "Lite" version we can calculate on frontend or just show counts if dataset is small.
                // For now, let's just show total employees.

                // Bonus: Get attendance for today
                // We'd need to fetch all attendance or filter by date on backend.
                // Let's stick to simple employee count for now to save time/complexity.

                setStats({
                    totalEmployees: employeesRes.data.length,
                    presentToday: 0 // Placeholder
                });
            } catch (error) {
                console.error("Failed to fetch dashboard stats", error);
            } finally {
                setLoading(false);
            }
        };

        fetchStats();
    }, []);

    return (
        <div className="space-y-6">
            <h1 className="text-3xl font-bold text-gray-800">Dashboard</h1>

            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
                <div className="bg-white p-6 rounded-lg shadow-md border-l-4 border-blue-500">
                    <h2 className="text-gray-500 text-sm font-medium uppercase">Total Employees</h2>
                    <p className="text-3xl font-bold text-gray-800 mt-2">
                        {loading ? '...' : stats.totalEmployees}
                    </p>
                </div>

                <div className="bg-white p-6 rounded-lg shadow-md border-l-4 border-green-500">
                    <h2 className="text-gray-500 text-sm font-medium uppercase">System Status</h2>
                    <p className="text-3xl font-bold text-green-600 mt-2">Active</p>
                </div>
            </div>

            <div className="bg-white p-6 rounded-lg shadow-md">
                <h2 className="text-xl font-semibold mb-4">Welcome to HRMS Lite</h2>
                <p className="text-gray-600">
                    Manage your employees and track daily attendance efficiently.
                    Use the navigation bar to access different sections.
                </p>
            </div>
        </div>
    );
};

export default Dashboard;
