import React, { useState, useEffect } from "react";
import { useContext } from "react";
import { MenuContext } from "../../context/LateralMenuContext";
import { QuestionContext } from "../../context/chatContext";
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import { faFile } from "@fortawesome/free-solid-svg-icons";
import useFetch from "../../hooks/useFetch";
import endpoints from "../../Endpoints/endpoints.jsx";
import userToken from "../../helpers/userToken";
const API_KEY = import.meta.env.VITE_API_KEY;

function LateralMenu() {
  const { menuStatus } = useContext(MenuContext);
  const { updateHistoryQuestions } = useContext(QuestionContext);

  const [trigger, setTrigger] = useState(true);

  const { data, error, loading } = useFetch(
    `${API_KEY}${endpoints.chat.HISTORY}`,
    "post",
    trigger,
    {
      prompt: "",
    },
    userToken()
  );

  const [history, setHistory] = useState([]);

  useEffect(() => {
    if (data?.chat_history) {
      let newHistory = [];
      let tempObj = {};

      for (let i = 0; i < data.chat_history.length; i++) {
        if (data.chat_history[i].role === "human") {
          tempObj.question = data.chat_history[i].message;
        }

        if (data.chat_history[i].role === "ai") {
          tempObj.ans = data.chat_history[i].message;
        }

        if (tempObj.question && tempObj.ans) {
          newHistory.push(tempObj);
          tempObj = {}; 
        }
      }

      setHistory(newHistory);
      setTrigger(false);
    }
  }, [data]);

  const handleHistoryItem = () => {
    updateHistoryQuestions(history);
  };

  return (
    <div
      className={
        menuStatus
          ? "w-3/12 pt-8 pb-8 "
          : "w-3/12 pt-8 pb-8 hidden  transition ease-in-out duration-500 "
      }
    >
      <div className="bg-white pt-8 pb-8 h-full rounded-2xl  ml-8">
        <h1 className="font-semibold mb-8 pl-4 pr-4">Reciente</h1>
        {history.length > 0 ? (
          <div className="mb-8 overflow-hidden text-ellipsis">
            <div
              onClick={handleHistoryItem}
              className="button mb-2  px-4 py-2 rounded-lg flex items-center cursor-pointer"
            >
              <FontAwesomeIcon className="pr-2 text-slate-400" icon={faFile} />
              Ultimas busquedas
            </div>
          </div>
        ) : (
          <div className="button mb-2  px-4 py-2 rounded-lg flex items-center cursor-pointer">
            No has realizado busquedas todavia
          </div>
        )}
      </div>
    </div>
  );
}

export default LateralMenu;
