import React, { useState } from "react";
import { useForm } from "react-hook-form";
import FormError from "../formError/FormError.jsx";
import { Link, useNavigate } from "react-router-dom";
import useFetch from "../../hooks/useFetch.jsx";
import { useEffect } from "react";
import { faArrowTurnUp } from "@fortawesome/free-solid-svg-icons";
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import ToastifyNotification from "../alerts/ToastifyNotification.jsx";
import endpoints from "../../Endpoints/endpoints.jsx";
const API_KEY = import.meta.env.VITE_API_KEY;

function LogInForm() {
  const [loginInfo, setLoginInfo] = useState({});
  const [trigger, setTrigger] = useState(false);
  const [errorAlert, setErrorAlert] = useState(false);
  const navigate = useNavigate();

  const {
    register,
    handleSubmit,
    formState: { errors },
  } = useForm();

  const onSubmit = (data) => {
    setLoginInfo(data);
    setTrigger(true);
    setErrorAlert(false);
  };

  const { data, error, loading } = useFetch(
    `${API_KEY}${endpoints.auth.LOGGIN}`,
    "post",
    trigger,
    loginInfo
  );

  useEffect(() => {
    if (data && data.token.length > 0) {
      localStorage.setItem("username", data.username);
      localStorage.setItem("token", data.token);
      navigate("/chat");
    } else {
    }
    setTrigger(false);
  }, [data, trigger]);

  useEffect(() => {
    if (error) {
      setErrorAlert(true);
    }
  }, [error]);

  return (
    <form
      action=""
      className="px-8 md:px-4 pt-8 pb-8 block max-w-xl w-full md:w-10/12"
      onSubmit={handleSubmit(onSubmit)}
    >
      <div className="flex justify-between  items-center mb-8">
        <h1 className="w-full  font-semibold text-2xl">Inicia sesión</h1>
        <Link to="/home">
          <FontAwesomeIcon
            className="text-[#7678ed] -rotate-90"
            icon={faArrowTurnUp}
          />
        </Link>
      </div>
      <div className="mb-3">
        <input
          autoComplete="off"
          className="w-full transition ease-in-out duration-500 rounded-lg p-4 bg-[#eeeef8] mt-1 focus:outline-none focus:border-sky-[#7678ed] focus:ring-2 focus:ring-[#7678ed]"
          type="text"
          placeholder="Correo electronico"
          {...register("email", {
            required: true,
            pattern: /^[a-zA-Z0-9_-]+@[a-zA-Z0-9_-]+\.[a-zA-Z0-9_-]+$/,
          })}
        />
        {errors?.email?.type == "required" && (
          <FormError message={"Ingresa tu correo electronico"} />
        )}
        {errors?.email?.type == "pattern" && (
          <FormError message={"Formato invalido"} />
        )}
      </div>
      <div>
        <input
          autoComplete="off"
          className="w-full transition ease-in-out duration-500 rounded-lg p-4 bg-[#eeeef8] mt-1 focus:outline-none focus:border-sky-[#7678ed] focus:ring-2 focus:ring-[#7678ed]"
          type="password"
          id="password"
          placeholder="Contraseña"
          {...register("password", {
            required: true,
          })}
        />
        {errors?.password?.type == "required" && (
          <FormError message={"Ingresa tu contraseña"} />
        )}
      </div>
      {loading ? (
        <button className="bg-[#7678ed] rounded-lg w-full p-4 mt-4 flex justify-center  text-white hover:bg-[#585aff] transition ease-in-out duration-300  font-semibold text-lgpointer-events: none">
          <svg
            className="animate-spin h-5 w-5 mr-4  bg-white"
            viewBox="0 0 24 24"
          ></svg>
          Iniciando sesion ...
        </button>
      ) : (
        <button className="bg-[#7678ed] rounded-lg w-full p-4 mt-4  text-white font-semibold text-lg hover:bg-[#585aff] transition ease-in-out duration-300 ">
          Ingresar
        </button>
      )}
      <div className="flex justify-between mb-4 text-sm text-slate-500  mt-4">
        <p>No estas registrado?</p>
        <Link to={"/sign-up"}>Registrate</Link>
      </div>
      {errorAlert === true && (
        <ToastifyNotification
          message="Email o contraseña incorrectos"
          type="error"
        />
      )}
    </form>
  );
}

export default LogInForm;
