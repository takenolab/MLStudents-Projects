import React, { useState, useEffect } from "react";
import io from "socket.io-client";
import "../App.css";
import { useNavigate } from 'react-router-dom';
const socket = io("http://localhost:8000");

const departments = [
  "IT", "Finance", "Transport", "Manufacturing",
  "Packaging", "Advertising", "Media", "Banking",
  "Legal", "HR", "Procurement", "Logistics"
];

const genders = ["Male", "Female", "Other"];

const AddEmployeeForm = () => {
  const [formData, setFormData] = useState({
    employee_name: "",
    employee_department: "",
    employee_role: "",
    employee_title:"",
    employee_email: "",
    employee_gender: ""
  });
  const navigate = useNavigate();
  const [loading, setLoading] = useState(false);
  const [successMsg, setSuccessMsg] = useState("");
  const [error, setError] = useState(null);

  useEffect(() => {
    const loadingTimeout = setTimeout(() => {
      if (loading) {
        setError("Employee addition timed out. Please try again.");
        setLoading(false);
      }
    }, 30000);  // Timeout after 30 seconds

    socket.on("employee_added", (data) => {
      setLoading(false);
      if (data.success) {
        setSuccessMsg(`Employee "${data.employee.employee_name}" added.`);
        setFormData({
          employee_name: "",
          employee_department: "",
          employee_role: "",
          employee_title:"",
          employee_email: "",
          employee_gender: ""
        });
        navigate("/chat")
      }
    });

    socket.on("error", (data) => {
      setLoading(false);
      setError(data.error || "Something went wrong.");
    });

    return () => {
      socket.off("employee_added");
      socket.off("error");
      clearTimeout(loadingTimeout);  // Cleanup timeout
    };
  }, [loading]);

  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData(prev => ({ ...prev, [name]: value }));
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    setLoading(true);
    setError(null);
    setSuccessMsg("");

    socket.emit("post_new_employee", formData);
  };

  return (
    <div className="add-employee-wrapper">
      <div className="add-employee-form-container">
        <h2>Add New Employee</h2>
        {error && <div className="form-error">{error}</div>}
        {successMsg && <div className="form-success">{successMsg}</div>}

        <form onSubmit={handleSubmit} className="add-employee-form">

          <input
            type="text"
            name="employee_name"
            placeholder="Full Name"
            value={formData.employee_name}
            onChange={handleChange}
            required
          />
        <input
            type="text"
            name="employee_title"
            placeholder="Employee Company Title"
            value={formData.employee_title}
            onChange={handleChange}
            required
          />
          <select
            name="employee_gender"
            value={formData.employee_gender}
            onChange={handleChange}
            required
          >
            <option value="">Select Gender</option>
            {genders.map((gender, idx) => (
              <option key={idx} value={gender}>{gender}</option>
            ))}
          </select>

          <select
            name="employee_department"
            value={formData.employee_department}
            onChange={handleChange}
            required
          >
            <option value="">Select Department</option>
            {departments.map((dept, idx) => (
              <option key={idx} value={dept}>{dept}</option>
            ))}
          </select>

          <input
            type="text"
            name="employee_role"
            placeholder="Role"
            value={formData.employee_role}
            onChange={handleChange}
            required
          />

          <input
            type="email"
            name="employee_email"
            placeholder="Email"
            value={formData.employee_email}
            onChange={handleChange}
            required
          />

          <button type="submit" disabled={loading}>
            {loading ? "Adding..." : "Add"}
          </button>
        </form>
      </div>
    </div>
  );
};

export default AddEmployeeForm;
