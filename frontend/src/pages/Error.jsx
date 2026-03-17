import React from "react";
import { Link } from "react-router-dom";
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import { faAngleLeft } from "@fortawesome/free-solid-svg-icons";

function Error() {
  return (
    <div className="min-h-screen flex justify-center items-center">
      <div>
        <h1 className="text-9xl font-bold mb-4 text-slate-500 text-center">
          404
        </h1>
        <h2 className="text-slate-400 text-center mb-6 font-semibold text-2xl">
          página no encontrada
        </h2>
        <div className="flex justify-center">
          <Link
            className="bg-[#7678ed] rounded-lg  p-2 px-20 text-center text-white font-semibold text-lg"
            to="/home"
          >
            <FontAwesomeIcon className="mr-8 font-bold" icon={faAngleLeft} />
            Volver
          </Link>
        </div>
      </div>
    </div>
  );
}

export default Error;
