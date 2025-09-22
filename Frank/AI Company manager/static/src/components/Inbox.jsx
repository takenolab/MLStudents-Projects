 import React, { useEffect, useState } from "react";
import { socket } from "./socket"; 
import "../App.css";

function ConversationPopup({ email, onClose }) {
  const [messages, setMessages] = useState([]);
  const [error, setError] = useState("");

  useEffect(() => {
    if (email) {
      socket.emit("get_employee_conversation", { employee_email: email });

      socket.on("employee_conversation", (data) => {
        if (data.success) {
          setMessages(data.conversation);
        } else {
          setError("Failed to load conversation.");
        }
      });

      socket.on("error", (err) => {
        setError(err?.error || "Unknown error occurred.");
      });
    }

    return () => {
      socket.off("employee_conversation");
      socket.off("error");
    };
  }, [email]);

  return (
    <div className="popup-overlay">
      <div className="popup-container">
        <button className="close-btn" onClick={onClose}>
          &times;
        </button>
        <h2>Conversation with <span>{email}</span></h2>
        {error && <p className="error">{error}</p>}
        {!error && messages.length > 0 ? (
          <div className="conversation-list">
            {messages.map((msg, index) => (
              <div className="message" key={index}>
                <p className="date">{msg.date}</p>
                {msg.subject && <p className="subject"><strong>{msg.subject}</strong></p>}
                <p className="body">{msg.body}</p>
              </div>
            ))}
          </div>
        ) : (
          !error && <p>Loading conversation...</p>
        )}
      </div>
    </div>
  );
}

export default ConversationPopup;
