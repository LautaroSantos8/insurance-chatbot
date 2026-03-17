import { ToastContainer, toast } from "react-toastify";
import "react-toastify/dist/ReactToastify.css";
import React, { useEffect } from "react";

function ToastifyNotification({ message, type }) {
  const notify = () => {
    toast[type](message, {
      toastId: message,
      position: "top-right",
      autoClose: 4000,
      hideProgressBar: false,
      closeOnClick: false,
      pauseOnHover: false,
      draggable: true,
      progress: undefined,
      theme: "light",
    });
  };
  useEffect(() => {
    if (message.length > 0) notify();
  }, [message, type]);

  return <ToastContainer />;
}

export default ToastifyNotification;
