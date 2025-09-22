import React, { useEffect, useState } from "react";
import { socket } from "./socket";
import "../App.css";
import userIcon from "./icons/account.png";
import ConversationPopup from "./Inbox";
import NotificationBadge from "./Badge";
import Sidebar from "./Header";

function EmployeeList() {
  const [employees, setEmployees] = useState([]);
  const [error, setError] = useState("");
  const [selectedEmail, setSelectedEmail] = useState("");

  useEffect(() => {
    socket.emit("get_employees");

    socket.on("employee_list_response", (data) => {
      if (data.success) {
        setEmployees(data.employees);
        setError("");
      } else {
        setEmployees([]);
        setError(data.message || "Failed to load employees.");
      }
    });

    return () => {
      socket.off("employee_list_response");
    };
  }, []);

  return (
    <>
      <Sidebar />
      <div className="employee-container">
        <h1 className="title">Stuff Room</h1>
        {error && <p className="error">{error}</p>}
        {!error && employees.length > 0 && (
          <div className="employee-list">
            {employees.map((emp) => (
              <div
                className="employee-card"
                key={emp.employee_id}
                onClick={() => setSelectedEmail(emp.employee_email)}
              >
                <img src={userIcon} alt="user" className="user-icon" />
                <div className="employee-info">
                  <p className="employee-name">Name: {emp.employee_name}</p>
                  <p className="employee-id">ID: {emp.employee_id}</p>
                  <p className="employee-gender">Title: {emp.employee_title}</p>
                  <p className="employee-department">Department: {emp.employee_department}</p>
                  <p className="employee-email">Email: {emp.employee_email}</p>
                </div>
 
                  <NotificationBadge email={emp.employee_email} />
 

                {/* Notification added here */}
              </div>
            ))}
          </div>
        )}

        {selectedEmail && (
          <ConversationPopup
            email={selectedEmail}
            onClose={() => setSelectedEmail("")}
          />
        )}
      </div>
    </>
  );
}

export default EmployeeList;
