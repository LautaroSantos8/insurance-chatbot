import React, { useState, createContext } from "react";

const MenuContext = createContext(null);

const MenuContextProvider = ({ children }) => {
  const [menuStatus, setMenuStatus] = useState(false);

  const updateMenuStatus = (menuStatus) => {
    setMenuStatus(menuStatus);
  };


  return (
    <MenuContext.Provider value={{ menuStatus, updateMenuStatus }}>
      {children}
    </MenuContext.Provider>
  );
};

export { MenuContext, MenuContextProvider };
