import React, { useEffect, useState } from "react";
import { socket } from "./socket";

function NotificationBadge({ email }) {
  const [count, setCount] = useState(0);
  const [hasNew, setHasNew] = useState(false);

  useEffect(() => {
    if (!email) return;

    // Join the room once
    socket.emit("join", { email });

    const handleNotification = (data) => {
      if (data.email === email) {
        console.log(`[RECV] ${email}:`, data);
        setHasNew(data.status);
        setCount(data.count || 0);
      }
    };

    socket.on("employee_notification", handleNotification);

    return () => {
      socket.off("employee_notification", handleNotification);
    };
  }, [email]);

  return (
    <div className="notification-badge">
      {hasNew && count > 0 ? (
        <span className="notification-ball blue">{count}</span> // Blue for new messages
      ) : (
        <span className="notification-ball gray">0</span> // Gray when no new messages
      )}
    </div>
  );
}

export default NotificationBadge;
