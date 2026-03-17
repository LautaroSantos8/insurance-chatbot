import React, { useState, useContext, useEffect } from "react";
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import {
  faPaperPlane,
  faMagnifyingGlass,
} from "@fortawesome/free-solid-svg-icons";
import { QuestionContext } from "../../context/chatContext";
import userToken from "../../helpers/userToken";
import useFetch from "../../hooks/useFetch";
import endpoints from "../../Endpoints/endpoints.jsx";
import ToastifyNotification from "../alerts/ToastifyNotification.jsx";

const API_KEY = import.meta.env.VITE_API_KEY;

function AskInput() {
  const [question, setQuestion] = useState("");
  const [trigger, setTrigger] = useState(false);
  const [questionsLength, setQuestionsLength] = useState(false);
  const [actualSearchingAlert, setActualSearchingAlert] = useState(null);

  const { updateQuestions, questions, updateQuickQuestions } =
    useContext(QuestionContext);

  //Obtener el hitorial
  const {
    data: history,
    error: herror,
    loading: hloading,
  } = useFetch(
    `${API_KEY}${endpoints.chat.HISTORY}`,
    "post",
    trigger,
    {
      prompt: "",
    },
    userToken()
  );

  const inputValue = (e) => {
    setQuestion(e.target.value);
  };

  const { data, error, loading } = useFetch(
    `${API_KEY}${endpoints.chat.GENERAL}`,
    "post",
    trigger,
    {
      prompt: question,
    },
    userToken()
  );

  const getQuestion = (e) => {
    e.preventDefault();
    if (question === "") {
      return;
    }
    setTrigger(true);
  };

  useEffect(() => {
    if (data != undefined && data != null) {
      updateQuestions({
        question,
        ans: data?.message,
      });
    }
    setTrigger(false);
    setQuestion("");
    updateQuickQuestions([]);
  }, [data]);

  useEffect(() => {
    if (questions.length > 0) {
      setQuestionsLength(true);
    } else {
      setQuestionsLength(false);
    }
  }, [questions]);

  return (
    <div className="px-4 sm:px-8 relative rounded-x pt-8 sm:pt-0 sm:-mt-6">
      <form className="rounded-xl relative">
        <input
          type="text"
          className="p-4 pr-20  sm:py-5 rounded-xl w-full text-lg  transition ease-in-out duration-500  bg-[#eeeef8] mt-1 focus:outline-none focus:border-sky-[#7678ed] focus:ring-2 focus:ring-[#7678ed]"
          onChange={inputValue}
          value={question}
        />
        {loading ? (
          <button className="absolute right-5 sm:right-10 top-1/2 transform -translate-y-1/2 font-bold text-slate-500 text-2xl pointer-events: none">
            <svg
              className="animate-spin h-5 w-5  bg-slate-500"
              viewBox="0 0 24 24"
            ></svg>
          </button>
        ) : (
          <button
            className="absolute right-5 sm:right-10 font-bold text-slate-500    top-1/2  transform  -translate-y-1/2"
            onClick={getQuestion}
          >
            <FontAwesomeIcon
              className="text-lg sm:text-xl"
              icon={faPaperPlane}
            />
          </button>
        )}
      </form>

      {actualSearchingAlert !== null && (
        <ToastifyNotification
          message={`Has activado la busqueda ${actualSearchingAlert}`}
          type="info"
        />
      )}
    </div>
  );
}

export default AskInput;
