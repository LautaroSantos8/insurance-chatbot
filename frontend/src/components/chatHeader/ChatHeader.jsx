import React, { useContext, useEffect, useState } from "react";
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import { MenuContext } from "../../context/LateralMenuContext";
import destroySession from "../../helpers/destroySession";
import useFetch from "../../hooks/useFetch";
import { QuickSearchContext } from "../../context/quickSearchContext";
import { QuestionContext } from "../../context/chatContext";
import ToastifyNotification from "../alerts/ToastifyNotification";
import QuickSearch from "../quickSearch/QuickSearch";

import {
  faRobot,
  faArrowRightFromBracket,
  faFolder,
  faEraser,
  faMagnifyingGlass,
  faXmark,
} from "@fortawesome/free-solid-svg-icons";
import endpoints from "../../Endpoints/endpoints";
const API_KEY = import.meta.env.VITE_API_KEY;
import userToken from "../../helpers/userToken";

function ChatHeader() {
  const { updateMenuStatus } = useContext(MenuContext);
  const { quickSearchStatus, updateQuickSearchStatus } =
    useContext(QuickSearchContext);
  const { resetQuestions } = useContext(QuestionContext);

  const [btn, setBtn] = useState(false);
  const [trigger, setUserTrigger] = useState(false);
  const [alert, setAlert] = useState(false);

  const handleSerch = (status) => {
    setBtn(!status);
  };

  useEffect(() => {
    updateMenuStatus(btn);
  }, [btn]);

  const { data } = useFetch(
    `${API_KEY}${endpoints.chat.RESET}`,
    "post",
    trigger,
    null,
    userToken()
  );

  const resetHistory = () => {
    setUserTrigger(true);
    setAlert(false);
    resetQuestions();
  };

  useEffect(() => {
    if (data != null) {
      setUserTrigger(false);
      setAlert(true);
    }
  }, [data]);

  const handleQuickSearch = () => {
    updateQuickSearchStatus(!quickSearchStatus);
  };

  return (
    <div className="text-slate-600  flex items-center justify-between  shadow-sm">
      <div className="flex items-center py-5 sm:py-7 px-4 sm:px-8 w-full justify-between">
        <div className="text-3xl flex items-center">
          <div className="w-8 sm:w-12  rounded-full overflow-hidden">
            <img className="w-full" src="./robot.png" alt="" />
          </div>

          <span className="text-sm sm:text-base ml-2 font-medium text-black flex">
            <span className="hidden sm:flex">Estamos: </span>
            <span className="ml-1 font-medium">Online</span>
          </span>
          <div className="inline-block bg-green-500 w-3 h-3 sm:w-4 sm:h-4 rounded-full ml-2"></div>
        </div>
        <div className="flex items-center">
          <div className="flex">
            <button
              className={` ${
                quickSearchStatus ? "sm:mr-0 mr-0" : "mr-3 sm:mr-6 "
              }`}
              onClick={handleQuickSearch}
            >
              <FontAwesomeIcon
                className="ml-1 rotate-90"
                icon={quickSearchStatus ? faXmark : faMagnifyingGlass}
              />
            </button>
            <QuickSearch />
          </div>
          <button
            className={`mr-3 sm:mr-6 text-xl ${quickSearchStatus && "hidden"}`}
            onClick={resetHistory}
          >
            <FontAwesomeIcon icon={faEraser} />
          </button>
          <button
            className={`mr-3 sm:mr-6 text-xl ${quickSearchStatus && "hidden"}`}
            onClick={() => handleSerch(btn)}
          >
            <FontAwesomeIcon icon={faFolder} />
          </button>

          <button
            onClick={() => destroySession()}
            className={`bg-slate-700 text-white font-semibold px-3 sm:px-5 rounded-xl py-0.5 sm:py-1 text-sm sm:text-base ${
              !quickSearchStatus ? "sm:px-2.5 rounded-md" : "px-1.5 sm:px-2"
            }`}
          >
            {!quickSearchStatus && "Salir"}

            <FontAwesomeIcon
              className={` ${quickSearchStatus ? "ml-0" : "ml-3"}`}
              icon={faArrowRightFromBracket}
            />
          </button>
        </div>
      </div>
      {alert && (
        <ToastifyNotification
          message="Se ha borrado el historial"
          type="info"
        />
      )}
    </div>
  );
}

export default ChatHeader;
