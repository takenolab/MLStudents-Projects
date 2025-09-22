import React, { useEffect, useState, useRef } from 'react';
import io from 'socket.io-client';

import '../App.css';

const socket = io('http://localhost:8000');

const GetConversation = () => {
  const [messages, setMessages] = useState([]);
  const messagesEndRef = useRef(null); // Create a ref to scroll to the bottom

  // Scroll to bottom whenever messages change
  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  useEffect(() => {
     
    socket.emit('get_conversation');

    socket.on('conversation_response', (data) => {
      if (data.success && Array.isArray(data.conversation)) {
        setMessages(data.conversation);
      }
    });

    socket.on('conversation_update', (data) => {
      if (data.success && Array.isArray(data.conversation)) {
        setMessages(data.conversation);
      }
    });

    return () => {
      socket.off('conversation_response');
      socket.off('conversation_update');
    };
  }, []);

  
  useEffect(() => {
    scrollToBottom();
  }, [messages]);  

  return (
    <div className="ai-messages-container">
      {messages.map((msg, idx) => (
        <div
          key={idx}
          className={`chat-bubble ${msg.role === 'user' ? 'user' : 'ai'}`}
        >
          {msg.content}
        </div>
      ))}
      {/* This is the element we scroll to */}
      <div ref={messagesEndRef} />
    </div>
  );
};

export default GetConversation;
