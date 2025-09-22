import React, { useEffect, useState } from "react";
import { Link } from "react-router-dom";
import io from "socket.io-client";
import "../App.css";

import chatIcon from "./icons/chat.png";
import inboxIcon from "./icons/no_mail.png";
import newInboxIcon from "./icons/new_mail.png";
import homeIcon from "./icons/home.png";
import addIcon from "./icons/add.png";
import search from "./icons/search.png"
import assign from "./icons/assign.png"

const socket = io("http://127.0.0.1:4000");

function Sidebar() {
  const [hasNewMessage, setHasNewMessage] = useState(false);

  useEffect(() => {
    socket.on("notification", (data) => {
      if (data && typeof data.status === "boolean") {
        setHasNewMessage(data.status);
      }
    });

    return () => {
      socket.off("notification");
    };
  }, []); 

  useEffect(() => {
    console.log("New message status:", hasNewMessage);
  }, [hasNewMessage]);

  const menuItems = [
    { label: "Home", icon: homeIcon, path: "/" },
    { label: "Chat", icon: chatIcon, path: "/chat" },
    { label: "Schedule", icon: assign, path: "/assign" },
     { label: "Search", icon: search, path: "/search" },
    {
      label: "Inbox",
      icon: hasNewMessage ? newInboxIcon : inboxIcon,
      path: "/employees",
      className: hasNewMessage ? "shake new-notification" : "",  // Add conditional class for shaking and color change
    },
    { label: "Add Employee", icon: addIcon, path: "/add" },
  ];

  return (
    <div className="sidebar">
      <div className="sidebar-header">
        <h1 className="sidebar-title">Goblin Inc</h1>
        <h2 className="sidebar-subtitle">MindMailer AI Assistant</h2>
      </div>

      <nav className="sidebar-menu">
        {menuItems.map((item) => (
          <Link to={item.path} key={item.label} className="sidebar-item">
            <img 
              src={item.icon} 
              alt={item.label} 
              className={`sidebar-icon ${item.className}`} // Apply the shake and color change classes
            />
            <span className="sidebar-label">{item.label}</span>
          </Link>
        ))}
      </nav>
    </div>
  );
}

export default Sidebar;
