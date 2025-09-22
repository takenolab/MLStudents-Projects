import React, { useEffect, useState } from "react";
import io from "socket.io-client";
import GetConversation from "./MessageBubble";
import Sidebar from "./Header";
import send from "./icons/send.png";
import loadingGif from "./icons/loading.gif";
import attachment from "./icons/attach_file.png";
import "../App.css";
import SidebarRight from "./Tool kit";
 

const socket = io("http://localhost:8000");

const SendMessage = () => {
  const [message, setMessage] = useState('');
  const [loading, setLoading] = useState(false);
  const [userMessages, setUserMessages] = useState([]);
  const [error, setError] = useState(null);

  useEffect(() => {
    socket.on('message_response', () => {
      setLoading(false);
    });

    socket.on('error', (data) => {
      setLoading(false);
      setError(data.error || "Unknown error");
      console.error('Socket Error:', data.error);
    });

    return () => {
      socket.off('message_response');
      socket.off('error');
    };
  }, []);

  useEffect(() => {
    if (error) {
      const timer = setTimeout(() => setError(null), 5000);
      return () => clearTimeout(timer);
    }
  }, [error]);

  const handleSend = () => {
    if (!message.trim() || loading) return;

    setUserMessages(prev => [...prev, { content: message, role: 'user' }]);
    setLoading(true);
    socket.emit('send_message', { user_text: message });
    setMessage('');
  };

  const handleKeyDown = (e) => {
    if (e.key === 'Enter') {
      e.preventDefault();
      handleSend();
    }
  };

  useEffect(() => {
    socket.on('conversation_update', (data) => {
      if (data.success) {
        setUserMessages(data.conversation);
        // scrollToBottom(); // REMOVED
      }
    });

    return () => socket.off('conversation_update');
  }, []);

  return (
    <>
      <Sidebar />
       
      <div className="chat-container">
        <GetConversation userMessages={userMessages} />

        {error && (
          <div className="error-popup">
            {error}
          </div>
        )}

        <div className="chat-input-container">
          <input type="file" id="csv-input" accept=".csv,text/csv" style={{ display: "none" }} />
          
          <label htmlFor="csv-input">
            <img src={attachment} alt="Attach File" className="attachment-icon" />
          </label>

          <textarea
            placeholder="Type your message..."
            value={message}
            onChange={(e) => setMessage(e.target.value)}
            onKeyDown={handleKeyDown}
            className="chat-input"
          />

          <img
            src={loading ? loadingGif : send}
            alt={loading ? "Loading..." : "Send"}
            className={`send-icon ${loading ? "disabled" : ""}`}
            onClick={!loading ? handleSend : null}
            style={{ cursor: loading ? "default" : "pointer" }}
          />
          
        </div>
      </div>
    </>
  );
};

export default SendMessage;
