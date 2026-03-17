import React from "react";
import { Link } from "react-router-dom";
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import {
  faFacebook,
  faSquareTwitter,
  faInstagram,
} from "@fortawesome/free-brands-svg-icons";

function Footer() {
  return (
    <div className="py-16 px-12 mt-22 bg-[#2c3e50]">
      <div className=" text-white flex flex-wrap justify-between max-w-7xl mx-auto">
        <div className="w-full md:w-6/12 lg:w-3/12 mb-8 lg:mb-0 text-center">
          <ul>
            <li className="font-semibold mb-2">Nuestra compañia</li>
            <li>
              <Link to="#">Nosotros</Link>
            </li>
            <li>
              <Link to="#">Servicios</Link>
            </li>
            <li>
              <Link to="#">Equipo</Link>
            </li>
            <li>
              <Link to="#">Contacto</Link>
            </li>
          </ul>
        </div>
        <div className="w-full md:w-6/12 lg:w-3/12 mb-8 lg:mb-0 text-center">
          <ul>
            <li className="font-semibold mb-2">Seguros</li>
            <li>
              <Link to="#"> Automóvil</Link>
            </li>
            <li>
              <Link to="#">Hogar</Link>
            </li>
            <li>
              <Link to="#">Salud</Link>
            </li>
            <li>
              <Link to="#">Vida</Link>
            </li>
          </ul>
        </div>
        <div className="w-full md:w-6/12 lg:w-3/12 mb-8 lg:mb-0 text-center">
          <ul>
            <li className="font-semibold mb-2">Recursos</li>
            <li>
              <Link to="#">Blog</Link>
            </li>
            <li>
              <Link to="#">Preguntas frecuentes</Link>
            </li>
            <li>
              <Link to="#">Centro de ayuda</Link>
            </li>
            <li>
              <Link to="#">Política de Privacidad</Link>
            </li>
          </ul>
        </div>
        <div className="w-full md:w-6/12 lg:w-3/12 text-center">
          <ul>
            <li className="font-semibold mb-2">Soporte</li>
            <li>
              <Link to="#">Atención al cliente</Link>
            </li>
            <li>
              <Link to="#">Contacto</Link>
            </li>
            <li>
              <Link to="#">Horarios de atención</Link>
            </li>
            <li>
              <Link to="#">FAQ</Link>
            </li>
          </ul>
        </div>
      </div>
      <div className="text-white mt-20 text-center flex justify-center">
        <ul className="text-2xl flex">
          <li className="mr-4">
            <Link to="#">
              <FontAwesomeIcon icon={faFacebook} />
            </Link>
          </li>
          <li className="mr-4">
            <Link to="#">
              <FontAwesomeIcon icon={faSquareTwitter} />
            </Link>
          </li>
          <li>
            <Link>
              <FontAwesomeIcon icon={faInstagram} />
            </Link>
          </li>
          <li></li>
        </ul>
      </div>
      <div className="text-white text-center mt-8">&copy; 2024</div>
    </div>
  );
}

export default Footer;
