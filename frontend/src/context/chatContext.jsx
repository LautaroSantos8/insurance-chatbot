import React, { useState, createContext, useEffect } from "react";
import { v4 as uuidv4 } from "uuid";

const QuestionContext = createContext(null);

const QuestionContextProvider = ({ children }) => {
  const [questions, setQuestions] = useState([]);
  const [quickQuestions, setQuickQuestions] = useState([]);


  const updateQuestions = (question) => {
    setQuestions([...questions, question]);
  };

  const resetQuestions = () => {
    setQuestions([]);
  };

  const updateHistoryQuestions = (questionsList) => {
    setQuestions([...questions, ...questionsList]);
  };


  const updateQuickQuestions = (historyQuestions) => {
    setQuickQuestions(historyQuestions);
  };

  return (
    <QuestionContext.Provider
      value={{
        questions,
        updateQuestions,
        updateHistoryQuestions,
        history,
        updateQuickQuestions,
        quickQuestions,
        resetQuestions,
      }}
    >
      {children}
    </QuestionContext.Provider>
  );
};

export { QuestionContext, QuestionContextProvider };
