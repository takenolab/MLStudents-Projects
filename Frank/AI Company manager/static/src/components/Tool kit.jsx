import React from "react";
import "../App.css";
import menuIcon from "./icons/clear.png"; 
import refreshIcon from "./icons/refreash.png";  

const SidebarRight = () => {
  const handleClick = (action) => {
    console.log(action);
  };

  return (
    <div className="sidebar">
      <img
        src={menuIcon}
        alt="Menu"
        className="icon"
        onClick={() => handleClick("Menu Clicked")}
      />
      <img
        src={refreshIcon}
        alt="Refresh"
        className="icon"
        onClick={() => handleClick("Refresh Clicked")}
      />
    </div>
  );
};

export default SidebarRight;
