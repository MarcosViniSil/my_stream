import { createContext, useState, useEffect } from "react";

export const ThemeContext = createContext();

export const ThemeProvider = ({ children }) => {
  const [theme, setTheme] = useState(() => {
    return localStorage.getItem("isDark") === "true";
  });

  const toggleTheme = () => {
    const newValue = !theme;
    localStorage.setItem("isDark", newValue);
    setTheme(newValue);
  };

    useEffect(() => {
    document.documentElement.classList.toggle("lightTheme", !theme);
    document.documentElement.classList.toggle("darkTheme", theme);
    const rootElement = document.getElementById("root");
  if (rootElement) {
    rootElement.classList.toggle("lightTheme", !theme);
    rootElement.classList.toggle("darkTheme", theme);
  }
  }, [theme]);

  return (
    <ThemeContext.Provider value={{theme, toggleTheme }}>
      {children}
    </ThemeContext.Provider>
  );
};
