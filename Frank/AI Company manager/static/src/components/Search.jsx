import React, { useState, useEffect } from "react";
import { io } from "socket.io-client";
import "../App.css";

import searchIcon from "./icons/search.png"; 

const socket = io("http://localhost:5000");

function SearchEmployee() {
  const [query, setQuery] = useState("");
  const [allEmployees, setAllEmployees] = useState([]);
  const [results, setResults] = useState([]);
  const [selectedEmployee, setSelectedEmployee] = useState(null);

  useEffect(() => {
 
    socket.emit("get_employees");

    socket.on("employee_list_response", (data) => {
      if (data.success) {
        setAllEmployees(data.employees);
      }
    });

    return () => {
      socket.off("employee_list_response");
    };
  }, []);

  useEffect(() => {
    if (query.trim() === "") {
      setResults([]);
      return;
    }

    const filtered = allEmployees.filter((emp) =>
      emp.employee_name.toLowerCase().includes(query.toLowerCase()) ||
      emp.employee_email.toLowerCase().includes(query.toLowerCase())
    );

    setResults(filtered);
  }, [query, allEmployees]);

  return (
    <div className="search-container">
      <div className="search-bar">
        <img src={searchIcon} alt="Search" className="search-icon" />
        <input
          type="text"
          placeholder="Search employees..."
          value={query}
          onChange={(e) => setQuery(e.target.value)}
        />
      </div>

      {results.length > 0 && (
        <div className="search-results">
          {results.map((emp) => (
            <div
              key={emp.employee_id}
              className="search-result-item"
              onClick={() => setSelectedEmployee(emp)}
            >
              {emp.employee_name} — <span>{emp.employee_email}</span>
            </div>
          ))}
        </div>
      )}

      {selectedEmployee && (
        <div className="employee-details">
          <h3>Employee Details</h3>
          <p><strong>Name:</strong> {selectedEmployee.employee_name}</p>
          <p><strong>Email:</strong> {selectedEmployee.employee_email}</p>
          <p><strong>Department:</strong> {selectedEmployee.employee_department}</p>
          <p><strong>Title:</strong> {selectedEmployee.employee_title}</p>
          <p><strong>Gender:</strong> {selectedEmployee.employee_gender}</p>
        </div>
      )}
    </div>
  );
}

export default SearchEmployee;
