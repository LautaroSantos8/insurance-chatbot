import React, { useState, useEffect } from "react";
import { useForm } from "react-hook-form";
import FormError from "../formError/FormError.jsx";
import { Link } from "react-router-dom";
import useFetch from "../../hooks/useFetch.jsx";
import { faArrowTurnUp } from "@fortawesome/free-solid-svg-icons";
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import ToastifyNotification from "../alerts/ToastifyNotification.jsx";
import { useNavigate } from "react-router-dom";
import endpoints from "../../Endpoints/endpoints.jsx";
const API_KEY = import.meta.env.VITE_API_KEY;

function SignUpForm() {
  const [confirmPasswordAlert, setConfirmPasswordAlert] = useState(false);
  const [userInfo, setUserInfo] = useState({});
  const [trigger, setTrigger] = useState(false);
  const [RegisteredEmailAlert, setRegisteredEmailAlert] = useState(false);
  const [errorAlert, setErrorAlert] = useState(false);
  const navigate = useNavigate();

  const {
    register,
    handleSubmit,
    watch,
    formState: { errors },
    reset,
  } = useForm();

  const onSubmit = (data) => {
    setRegisteredEmailAlert(false);
    if (password === confirmPassword) {
      delete data.confirmPassword;
      setUserInfo({
        ...data,
      });
      setTrigger(true);
      setErrorAlert(false);
    }
  };

  const password = watch("password");
  const confirmPassword = watch("confirmPassword");

  useEffect(() => {
    if (
      password &&
      password.length > 0 &&
      confirmPassword &&
      confirmPassword.length > 0
    ) {
      if (password === confirmPassword) {
        setConfirmPasswordAlert(false);
      } else {
        setConfirmPasswordAlert(true);
      }
    }
  }, [password, confirmPassword]);

  const { data, error, loading } = useFetch(
    `${API_KEY}${endpoints.auth.SIGN_UP}`,
    "post",
    trigger,
    userInfo
  );

  useEffect(() => {
    setTrigger(false);
    if (data?.status === 400) {
      setRegisteredEmailAlert(true);
    }
    if (data !== null && data?.token) {
      setRegisteredEmailAlert(false);
      navigate("/log-in");
      reset();
    }
    setUserInfo({});
  }, [data]);

  useEffect(() => {
    if (error) {
      setErrorAlert(true);
    }
  }, [error, trigger]);

  return (
    <form
      className="px-8 md:px-4 pt-8 pb-8 block max-w-xl w-full md:w-10/12"
      onSubmit={handleSubmit(onSubmit)}
    >
      <div className="flex justify-between  items-center mb-8">
        <h1 className="w-full  font-semibold text-2xl">Registrate</h1>
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
          id="user"
          className="w-full transition ease-in-out duration-500 rounded-lg p-4 bg-[#eeeef8] mt-1 focus:outline-none focus:border-sky-[#7678ed] focus:ring-2 focus:ring-[#7678ed]"
          type="text"
          placeholder="Usuario"
          {...register("username", {
            required: true,
            pattern: /^[a-zA-Z0-9\s_-]*$/,
          })}
        />
        {errors?.username?.type == "required" && (
          <FormError message={"Ingresa tu nombre de usuario"} />
        )}
        {errors?.username?.type == "pattern" && (
          <FormError message={"No se permiten caracteres especiales"} />
        )}
      </div>
      <div className="mb-3">
        <input
          autoComplete="off"
          id="email"
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
      <div className="mb-3">
        <input
          autoComplete="off"
          className="w-full transition ease-in-out duration-500 rounded-lg p-4 bg-[#eeeef8] mt-1 focus:outline-none focus:border-sky-[#7678ed] focus:ring-2 focus:ring-[#7678ed]"
          type="password"
          id="password"
          placeholder="Contraseña"
          {...register("password", {
            required: true,
            pattern: /^(?=.*[a-zA-Z\d])[a-zA-Z\d*\-?]{5,}$/,
          })}
        />
        {errors?.password?.type == "required" && (
          <FormError message={"Ingresa tu contraseña"} />
        )}
        {errors?.password?.type == "pattern" && (
          <FormError
            message={
              "La contraseña debe tener minimo 5 caracteres incluyendo -?*"
            }
          />
        )}
      </div>
      <div>
        <input
          autoComplete="off"
          className="w-full transition ease-in-out duration-500 rounded-lg p-4 bg-[#eeeef8] mt-1 focus:outline-none focus:border-sky-[#7678ed] focus:ring-2 focus:ring-[#7678ed]"
          type="password"
          placeholder="Confirmar contraseña"
          {...register("confirmPassword", {
            required: true,
            pattern: /^(?=.*[a-zA-Z\d])[a-zA-Z\d*\-?]{5,}$/,
          })}
        />
        {errors?.confirmPassword?.type == "required" && (
          <FormError message={"Confirma tu contraseña"} />
        )}
        {confirmPasswordAlert && (
          <FormError message="Las contraseñas no coinciden" />
        )}
      </div>
      {loading ? (
        <button className="bg-[#7678ed] rounded-lg w-full p-4 mt-4 flex justify-center  text-white hover:bg-[#585aff] transition ease-in-out duration-300  font-semibold text-lgpointer-events: none">
          <svg
            className="animate-spin h-5 w-5 mr-4  bg-white"
            viewBox="0 0 24 24"
          ></svg>
          Registrando...
        </button>
      ) : (
        <button className="bg-[#7678ed] rounded-lg w-full p-4 mt-5  text-white font-semibold text-lg hover:bg-[#585aff] transition ease-in-out duration-300 ">
          Registrar
        </button>
      )}
      <div className="flex justify-between mb-4 text-sm text-slate-500 mt-4">
        <p>Ya estas registrado?</p>
        <Link to={"/log-in"}>Inicia sesión</Link>
      </div>
      {RegisteredEmailAlert === true && (
        <ToastifyNotification
          className="absolute"
          message="Este email ya està registrado"
          type="info"
        />
      )}
      {errorAlert === true && (
        <ToastifyNotification
          message="Ha ocurrido un error inesperado"
          type="error"
        />
      )}
    </form>
  );
}

export default SignUpForm;
