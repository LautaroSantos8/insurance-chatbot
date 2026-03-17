import React, { useContext, useRef, useEffect, useState } from "react";
import { QuestionContext } from "../../context/chatContext";
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import { faUser } from "@fortawesome/free-solid-svg-icons";
import Modal from "../modal/Modal";
import "./pending.css";
import ReactMarkdown from "react-markdown";

function Pending() {
  const { questions } = useContext(QuestionContext);

  const elementRef = useRef(null);

  useEffect(() => {
    if (elementRef.current && questions && questions?.length > 0) {
      elementRef.current.scroll({
        top: elementRef.current.scrollHeight,
        behavior: "smooth",
      });
    }
  }, [questions]);

  return (
    <div className="relative">
      <div
        ref={elementRef}
        className={
          questions?.length > 0
            ? "h-[calc(100vh-250px)]  py-8 px-4 sm:px-8 text-white overflow-y-scroll pending"
            : "h-[calc(100vh-250px)]  py-8 px-4 sm:px-8 text-white overflow-y-scroll pending flex  items-center justify-center"
        }
      >
        {questions?.length > 0 ? (
          <div>
            {questions?.map((question) => {
              return (
                <div key={question.question} classname="question">
                  <div className="max-w-xl flex items-center ">
                    <FontAwesomeIcon
                      className="mr-3  text-slate-500 rounded-full -mt-3 text-base"
                      icon={faUser}
                    />
                    <div className="bg-[#f1f1fb] rounded-2xl p-4 inline-block mt-5  text-[#7678ed]">
                      {question?.question}
                    </div>
                  </div>
                  {Array.isArray(question?.ans) ? (
                    <div className="flex justify-end items-start  question">
                      <div className="w-8 rounded-full mt-5 mr-2 overflow-hidden">
                        <img
                          className="w-full  object-cover"
                          src="./robot.png"
                          alt="robot"
                        />
                      </div>
                    </div>
                  ) : (
                    <div className="flex justify-end items-start  question">
                      <div className="w-8 rounded-full mt-5 mr-2 overflow-hidden">
                        <img
                          className="w-full  object-cover"
                          src="./robot.png"
                          alt="robot"
                        />
                      </div>
                      <div className="bg-[#7678ed] rounded-2xl p-4 inline-block mt-6 max-w-xl">
                        <ReactMarkdown>{question?.ans}</ReactMarkdown>
                        <div
                        />
                      </div>
                    </div>
                  )}
                </div>
              );
            })}
          </div>
        ) : (
          <div>
            <div className="text-xl rounded-2xl p-12 w-full sm:w-8/12 mx-auto ">
              <div className="text-4xl sm:text-5xl text-left text-slate-500 font-semibold">
                Hola{" "}
                <span className="text-[#7678ed]" id="userName">
                  {localStorage.getItem("username")}
                </span>
              </div>
              <div className="text-left text-slate-500 font-semibold text-base sm:text-xl">
                Soy tu asistente virtual, pregúntame sobre tu póliza de seguros.
              </div>
            </div>
          </div>
        )}
      </div>
      <Modal />
    </div>
  );
}

export default Pending;
