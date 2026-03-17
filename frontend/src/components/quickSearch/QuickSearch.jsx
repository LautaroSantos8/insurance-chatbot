import React, { useContext, useState, useEffect } from "react";
import { QuickSearchContext } from "../../context/quickSearchContext";
import useFetch from "../../hooks/useFetch";
const API_KEY = import.meta.env.VITE_API_KEY;
import endpoints from "../../Endpoints/endpoints.jsx";
import userToken from "../../helpers/userToken";
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import { faMagnifyingGlass } from "@fortawesome/free-solid-svg-icons";

import { QuestionContext } from "../../context/chatContext";

function QuickSearch() {
  const [question, setQuestion] = useState("");
  const [trigger, setTrigger] = useState(false);
  const { quickSearchStatus, updateQuickSearchStatus } =
    useContext(QuickSearchContext);
  const { updateQuestions, questions, updateQuickQuestions, quickQuestions } =
    useContext(QuestionContext);

  const inputValue = (e) => {
    setQuestion(e.target.value);
  };

  const { data, error, loading } = useFetch(
    `${API_KEY}${endpoints.chat.QUICK}`,
    "post",
    trigger,
    {
      query: question,
    },
    userToken()
  );

  useEffect(() => {
    if (data != undefined && data != null) {
      updateQuickQuestions({
        question,
        ans: data?.message,
      });
      updateQuickSearchStatus(false);
    }
    setTrigger(false);
    setQuestion("");
  }, [data]);

  const getQuestion = (e) => {
    e.preventDefault();
    if (question === "") {
      return;
    }
    setTrigger(true);
  };

  return (
    <div className={quickSearchStatus ? "block relative" : "hidden"}>
      <h1>{quickSearchStatus}</h1>
      <form className="px-2 relative">
        <input
          className="text-black block py-1.5 pr-14  rounded-xl w-full text-lg  transition ease-in-out duration-500  bg-[#eeeef8] focus:outline-none focus:border-sky-[#7678ed] focus:ring-2 focus:ring-[#7678ed] px-4"
          type="text"
          placeholder="Busqueda rapida"
          onChange={inputValue}
          value={question}
        />

        {loading ? (
          <button className="absolute right-4 sm:mr-2  top-1/2 transform -translate-y-1/2 font-bold text-slate-500 text-2xl pointer-events: none">
            <svg
              className="animate-spin h-4 w-4  bg-slate-500"
              viewBox="0 0 24 24"
            ></svg>
          </button>
        ) : (
          <button
            className="right-4 sm:mr-2  text-xl text-slate-500 absolute top-1/2  transform  -translate-y-1/2 "
            onClick={getQuestion}
          >
            <FontAwesomeIcon
              className="ml-1 rotate-90"
              icon={faMagnifyingGlass}
            />
          </button>
        )}
      </form>
    </div>
  );
}

export default QuickSearch;
