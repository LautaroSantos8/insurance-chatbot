import { useState, useContext, useCallback, useEffect } from "react";
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import { faPaperPlane } from "@fortawesome/free-solid-svg-icons";
import { QuestionContext } from "../../context/chatContext";
import userToken from "../../helpers/userToken";
import endpoints from "../../Endpoints/endpoints.jsx";
import ToastifyNotification from "../alerts/ToastifyNotification.jsx";
const API_KEY = import.meta.env.VITE_API_KEY;

function AskInputStream() {
  const [question, setQuestion] = useState("");
  const [answer, setAnswer] = useState("");
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(false);

  const { updateQuestions, updateQuickQuestions } = useContext(QuestionContext);

  const inputValue = (e) => {
    setQuestion(e.target.value);
  };

  const askInputStream = useCallback(async () => {
    setLoading(true);
    setAnswer("");

    try {
      const response = await fetch(`${API_KEY}${endpoints.chat.STREAM}`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          Authorization: `Bearer ${userToken()}`,
        },
        body: JSON.stringify({ prompt: question }),
      });

      if (!response.ok) {
        setError(true);
        throw new Error("Network response was not ok");
      }
      setError(false);
      const reader = response.body.getReader();
      const decoder = new TextDecoder("utf-8");

      let result = "";
      let done = false;
      const chunks = [];

      while (!done) {
        const { value, done: readerDone } = await reader.read();
        done = readerDone;

        // if (value) {
        //   const chunk = decoder.decode(value, { stream: true });
        //   result += chunk;
        //   updateQuestions({
        //     question,
        //     ans: result,
        //   });
        // }
        if (value) {
          const chunk = decoder.decode(value, { stream: true });
          chunks.push(chunk);
        }
      }

      const processChunks = async () => {
        for (let chunk of chunks) {
          await new Promise((resolve) => {
            let currentIndex = 0;
            const intervalId = setInterval(() => {
              if (currentIndex < chunk.length) {
                result += chunk[currentIndex];
                currentIndex++;

                updateQuestions({
                  question,
                  ans: result,
                });
              } else {
                clearInterval(intervalId);
                resolve();
              }
            }, 5); 
          });
        }
      };

      await processChunks();

      setQuestion("");
      updateQuickQuestions([]);
    } catch (error) {
      console.error("Error in streaming response:", error);
    } finally {
      setLoading(false);
    }
  }, [question, updateQuestions]);

  const getQuestion = (e) => {
    e.preventDefault();
    if (question === "") {
      return;
    }
    askInputStream();
  };

  return (
    <div className="col-span-8 px-8 relative rounded-xl -mt-5">
      <form action="" className="rounded-xl">
        <input
          type="text"
          className="p-4 pr-20 py-5 rounded-xl w-full text-lg transition ease-in-out duration-500 bg-[#eeeef8] mt-1 focus:outline-none focus:border-sky-[#7678ed] focus:ring-2 focus:ring-[#7678ed]"
          onChange={inputValue}
          value={question}
        />
        {loading ? (
          <button className="absolute right-14 top-1/2 transform -translate-y-1/2 font-bold text-slate-500 text-2xl pointer-events: none">
            <svg
              className="animate-spin h-5 w-5 bg-slate-500"
              viewBox="0 0 24 24"
            ></svg>
          </button>
        ) : (
          <button
            className="absolute right-14 font-bold text-slate-500 text-2xl top-1/2 transform -translate-y-1/2"
            onClick={getQuestion}
          >
            <FontAwesomeIcon icon={faPaperPlane} />
          </button>
        )}
      </form>
      {/* <div className="mt-4">
        <h3>Answer:</h3>
        <p>{answer}</p>
      </div> */}
      {error === true && (
        <ToastifyNotification
          message="Ha ocurrido un error inesperado intenta limpiar el historial"
          type="error"
        />
      )}
    </div>
  );
}

export default AskInputStream;
