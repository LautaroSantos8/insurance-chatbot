import React from "react";
import ChatHeader from "../components/chatHeader/ChatHeader";
// import AskInput from "../components/askInput/AskInput";
import AskInputStream from "../components/askInputStream/AskInputStream";
import Pending from "../components/pending/Pending";
import LateralMenu from "../components/lateralMenu/LateralMenu";

function Chat() {
  return (
    <div className="bg-[#ecf0f1] min-h-screen flex justify-center">
      <LateralMenu />
      <div className="overflow-hidden  bg-white mt-8 mb-9 rounded-3xl shadow-lg mx-5 sm:w-10/12 max-w-3xl">
        <div>
          <ChatHeader />
        </div>
        <div>
          <Pending />
        </div>
        <div>{/* <AskInput /> */}</div>
        <div>
          <AskInputStream />
        </div>
      </div>
    </div>
  );
}

export default Chat;
