import { createContext, useState, useEffect } from "react";

export const AccessibleContext = createContext();

export const AccessibleProvider = ({ children }) => {
  const [accessible, setAccessible] = useState(() => {
    return localStorage.getItem("accessible") === "true";
  });

  const toggleAccessible = () => {
    const newValue = !accessible;
    localStorage.setItem("accessible", newValue);
    setAccessible(newValue);
  };

  return (
    <AccessibleContext.Provider value={{ accessible, toggleAccessible }}>
      {children}
    </AccessibleContext.Provider>
  );
};
