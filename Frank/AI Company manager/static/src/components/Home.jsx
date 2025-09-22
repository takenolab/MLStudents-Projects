import React from "react";
import { Link } from "react-router-dom";
import "../App.css";  

import chatIcon from "./icons/chat-bot.gif"; 
import inboxIcon from "./icons/mange.gif";  
import addIcon from "./icons/add-emp.gif"; 

const Home = () => {
  return (
    <div className="home-container">
      <div className="home-card">
        <Link to="/chat" className="home-card-link">
          <div className="card-icon">
            <img src={chatIcon} alt="AI Chat" />
          </div>
          <div className="card-title">MindMailer</div>
          <div className="card-description">Start a conversation with the MindMailer your AI assistant.</div>
        </Link>
      </div>

      <div className="home-card">
        <Link to="/employees" className="home-card-link">
          <div className="card-icon">
            <img src={inboxIcon} alt="Employee Inbox" />
          </div>
          <div className="card-title">Employee Inbox</div>
          <div className="card-description">View and manage employee communications.</div>
        </Link>
      </div>

      <div className="home-card">
        <Link to="/add" className="home-card-link">
          <div className="card-icon">
            <img src={addIcon} alt="Add Employee" />
          </div>
          <div className="card-title">Add Employee</div>
          <div className="card-description">Add new employees to the system.</div>
        </Link>
      </div>
    </div>
  );
};

export default Home;
