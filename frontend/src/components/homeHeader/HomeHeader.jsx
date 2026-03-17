import React from "react";
import { Link } from "react-router-dom";
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import { faUser } from "@fortawesome/free-solid-svg-icons";

function HomeHeader() {
  return (
    <div className="p-8 px-8 shadow-sm">
      <header className="flex justify-between items-center">
        <div className="text-slate-700 text-2xl sm:text-3xl flex items-center">
          <img src="logo.png" alt="YESID logo" width="40" height="40" />
          <span className="text-sm sm:text-lg font-semibold border-b-2 -mt-1.5 ml-1.5  border-b-[#7678ed] ">
            Y.E.S.I.D. Seguros
          </span>
        </div>
        <nav>
          <ul className="flex items-center">
            <li className="sm:px-4 text-sm sm:text-base">
              <Link to="/sign-up">Registrate</Link>
            </li>
            <li className="px-2 sm:px-4 bg-[#7678ed] rounded-lg font-semibold text-white py-1 sm:py-1.5 ml-4 hover:bg-[#585aff] transition ease-in-out duration-300 ">
              <Link
                to="/log-in"
                className="text-sm sm:text-base flex items-center "
              >
                Ingresa
                <FontAwesomeIcon className="ml-2 sm:ml-4" icon={faUser} />
              </Link>
            </li>
          </ul>
        </nav>
      </header>
    </div>
  );
}

export default HomeHeader;
