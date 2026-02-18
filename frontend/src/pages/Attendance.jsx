import React, { useState, useEffect } from 'react';
import api from '../services/api';
import { FaCalendarCheck, FaHistory } from 'react-icons/fa';

const Attendance = () => {
    const [employees, setEmployees] = useState([]);
    const [selectedEmployee, setSelectedEmployee] = useState('');
    const [date, setDate] = useState(new Date().toISOString().split('T')[0]);
    const [status, setStatus] = useState('Present');
    const [message, setMessage] = useState({ type: '', text: '' });
    const [attendanceRecords, setAttendanceRecords] = useState([]);
    const [viewEmployeeId, setViewEmployeeId] = useState('');

    // Fetch employees for dropdowns
    useEffect(() => {
        const fetchEmps = async () => {
            try {
                const res = await api.get('/employees/');
                setEmployees(res.data);
            } catch (err) {
                console.error("Failed to fetch employees", err);
            }
        };
        fetchEmps();
    }, []);

    const handleMarkAttendance = async (e) => {
        e.preventDefault();
        if (!selectedEmployee) {
            setMessage({ type: 'error', text: 'Please select an employee' });
            return;
        }

        try {
            await api.post('/attendance/', {
                employee_id: selectedEmployee,
                date: date,
                status: status
            });
            setMessage({ type: 'success', text: 'Attendance marked successfully!' });
            // Clear message after 3 seconds
            setTimeout(() => setMessage({ type: '', text: '' }), 3000);
        } catch (err) {
            setMessage({ type: 'error', text: err.response?.data?.detail || 'Failed to mark attendance' });
        }
    };

    const handleViewRecords = async () => {
        if (!viewEmployeeId) return;
        try {
            const res = await api.get(`/attendance/${viewEmployeeId}`);
            setAttendanceRecords(res.data);
        } catch (err) {
            console.error(err);
            setAttendanceRecords([]);
        }
    };

    useEffect(() => {
        if (viewEmployeeId) {
            handleViewRecords();
        }
    }, [viewEmployeeId]);


    return (
        <div className="space-y-8">
            <h1 className="text-3xl font-bold text-gray-800">Attendance Management</h1>

            <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
                {/* Mark Attendance Section */}
                <div className="bg-white rounded-lg shadow-md p-6">
                    <h2 className="text-xl font-semibold mb-4 flex items-center gap-2 border-b pb-2">
                        <FaCalendarCheck className="text-blue-500" /> Mark Attendance
                    </h2>

                    {message.text && (
                        <div className={`p-4 mb-4 rounded-md ${message.type === 'error' ? 'bg-red-50 text-red-700' : 'bg-green-50 text-green-700'}`}>
                            {message.text}
                        </div>
                    )}

                    <form onSubmit={handleMarkAttendance} className="space-y-4">
                        <div>
                            <label className="block text-sm font-medium text-gray-700">Select Employee</label>
                            <select
                                className="mt-1 block w-full border border-gray-300 rounded-md shadow-sm py-2 px-3 focus:outline-none focus:ring-blue-500 focus:border-blue-500 sm:text-sm"
                                value={selectedEmployee}
                                onChange={(e) => setSelectedEmployee(e.target.value)}
                                required
                            >
                                <option value="">-- Select Employee --</option>
                                {employees.map(emp => (
                                    <option key={emp.employee_id} value={emp.employee_id}>
                                        {emp.name} ({emp.employee_id})
                                    </option>
                                ))}
                            </select>
                        </div>

                        <div>
                            <label className="block text-sm font-medium text-gray-700">Date</label>
                            <input
                                type="date"
                                required
                                value={date}
                                onChange={(e) => setDate(e.target.value)}
                                className="mt-1 block w-full border border-gray-300 rounded-md shadow-sm py-2 px-3 focus:outline-none focus:ring-blue-500 focus:border-blue-500 sm:text-sm"
                            />
                        </div>

                        <div>
                            <label className="block text-sm font-medium text-gray-700">Status</label>
                            <select
                                className="mt-1 block w-full border border-gray-300 rounded-md shadow-sm py-2 px-3 focus:outline-none focus:ring-blue-500 focus:border-blue-500 sm:text-sm"
                                value={status}
                                onChange={(e) => setStatus(e.target.value)}
                            >
                                <option value="Present">Present</option>
                                <option value="Absent">Absent</option>
                            </select>
                        </div>

                        <button
                            type="submit"
                            className="w-full bg-blue-600 hover:bg-blue-700 text-white font-medium py-2 px-4 rounded-md shadow-sm transition-colors"
                        >
                            Mark Attendance
                        </button>
                    </form>
                </div>

                {/* View Records Section */}
                <div className="bg-white rounded-lg shadow-md p-6">
                    <h2 className="text-xl font-semibold mb-4 flex items-center gap-2 border-b pb-2">
                        <FaHistory className="text-green-500" /> View Records
                    </h2>

                    <div className="mb-4">
                        <label className="block text-sm font-medium text-gray-700">Select Employee to View</label>
                        <select
                            className="mt-1 block w-full border border-gray-300 rounded-md shadow-sm py-2 px-3 focus:outline-none focus:ring-green-500 focus:border-green-500 sm:text-sm"
                            value={viewEmployeeId}
                            onChange={(e) => setViewEmployeeId(e.target.value)}
                        >
                            <option value="">-- Select Employee --</option>
                            {employees.map(emp => (
                                <option key={emp.employee_id} value={emp.employee_id}>
                                    {emp.name} ({emp.employee_id})
                                </option>
                            ))}
                        </select>
                    </div>

                    <div className="overflow-y-auto max-h-64">
                        {viewEmployeeId && attendanceRecords.length === 0 ? (
                            <p className="text-gray-500 text-center py-4">No records found.</p>
                        ) : (
                            <table className="min-w-full divide-y divide-gray-200">
                                <thead className="bg-gray-50 sticky top-0">
                                    <tr>
                                        <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Date</th>
                                        <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Status</th>
                                    </tr>
                                </thead>
                                <tbody className="bg-white divide-y divide-gray-200">
                                    {attendanceRecords.map((record) => (
                                        <tr key={record._id || record.id}>
                                            <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-900">{record.date}</td>
                                            <td className="px-6 py-4 whitespace-nowrap text-sm">
                                                <span className={`px-2 inline-flex text-xs leading-5 font-semibold rounded-full ${record.status === 'Present' ? 'bg-green-100 text-green-800' : 'bg-red-100 text-red-800'
                                                    }`}>
                                                    {record.status}
                                                </span>
                                            </td>
                                        </tr>
                                    ))}
                                </tbody>
                            </table>
                        )}
                    </div>
                </div>
            </div>
        </div>
    );
};

export default Attendance;
