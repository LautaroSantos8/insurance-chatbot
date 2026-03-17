import React, { useContext } from "react";
import { QuestionContext } from "../../context/chatContext";
import "./modal.css";
import { faXmark } from "@fortawesome/free-solid-svg-icons";
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import ReactMarkdown from "react-markdown";

function Modal() {
  const { questions, updateQuickQuestions, quickQuestions } =
    useContext(QuestionContext);

  const handleClose = () => {
    updateQuickQuestions([]);
  };

  return (
    <>
      <div
        className={`absolute modal  overflow-hidden top-5 p-5 mx-8 right-0 left-0 bg-white z-50 rounded-2xl shadow-sm border border-slate-200 max-h-[600px] overflow-y-scroll  ${
          quickQuestions.length === 0
            ? "mt-[-100%] transition-all transition-duration: transition-duration: 50000ms transition-timing-function: cubic-bezier(0.4, 0, 0.2, 1)"
            : "mt-0 transition-all transition-duration: 50000ms transition-timing-function: cubic-bezier(0.4, 0, 0.2, 1)"
        }`}
      >
        <div className="flex justify-between items-center">
          <p className="bg-[#7678ed] text-white inline-block px-4 py-2 rounded-xl mb-2 ">
            {quickQuestions.question}
          </p>
          <button onClick={handleClose}>
            <FontAwesomeIcon
              className="ml-1 rotate-90 text-slate-600"
              icon={faXmark}
            />
          </button>
        </div>

        <p className="bg-[#eeeef8] rounded-2xl p-6 mt-1 ">
          {questions.length <= 5 &&
            quickQuestions?.ans?.slice(0, 8).map((res) => {
              return (
                <div className="mb-4" key={res.code}>
                  <div>
                    <span className="font-semibold">Codigo: </span>
                    {res.code}
                  </div>
                  <div>{res.title}</div>
                </div>
              );
            })}
        </p>
      </div>
    </>
  );
}

export default Modal;
