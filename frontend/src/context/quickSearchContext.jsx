import React, { useState, createContext } from "react";

const QuickSearchContext = createContext(null);

const QuickSearchProvider = ({ children }) => {
  const [quickSearchStatus, setQuickSearchStatus] = useState(false);

  const updateQuickSearchStatus = (quickSearchStatus) => {
    setQuickSearchStatus(quickSearchStatus);
  };

  return (
    <QuickSearchContext.Provider
      value={{ quickSearchStatus, updateQuickSearchStatus }}
    >
      {children}
    </QuickSearchContext.Provider>
  );
};

export { QuickSearchContext, QuickSearchProvider };
