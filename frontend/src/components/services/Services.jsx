import React from "react";
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import {
  faPersonDigging,
  faHouse,
  faUserNurse,
  faIndustry,
} from "@fortawesome/free-solid-svg-icons";

function Services() {
  return (
    <div className="flex flex-wrap lg:flex-nowrap  lg:gap-5 mt-20 justify-between">
      <div className="border border-slate-200 rounded w-full mb-5 lg:mb-0 sm:w-[calc(50%-10px)] lg:w-3/12 p-4 lg:p-8 flex flex-col justify-between">
        <div>
          <div className="text-center text-3xl mb-8  text-[#7678ed] ">
            <FontAwesomeIcon icon={faPersonDigging} />
          </div>
          <h2 className="text-center mb-6 font-semibold text-lg">
            Trabajadores
          </h2>
          <p className="text-center">
            Nuestro compromiso es asegurar la protección de los trabajadores de
            tu empresa. Con nuestras pólizas de seguros sólidas, brindamos
            tranquilidad y seguridad a cada empleado. Desde cobertura médica
            hasta protección laboral.
          </p>
        </div>
        <button className="px-4 mt-7 w-full bg-[#7678ed] rounded-lg font-semibold text-white py-2 hover:bg-[#585aff] transition ease-in-out duration-300 ">
          Conoce mas
        </button>
      </div>
      <div className="border border-slate-200 rounded w-full mb-5 lg:mb-0 sm:w-[calc(50%-10px)] lg:w-3/12 p-4 lg:p-8 flex flex-col justify-between">
        <div>
          <div className="text-center text-3xl mb-8 text-[#7678ed]">
            <FontAwesomeIcon icon={faHouse} />
          </div>
          <h2 className="text-center mb-6 font-semibold  text-lg">Hogar</h2>
          <p className="text-center">
            Nos dedicamos a proteger tu hogar y todo lo que amas. Con nuestras
            pólizas de seguros sólidas, brindamos una cobertura completa para tu
            tranquilidad. Desde incendios hasta robos, estamos aquí para
            asegurar que tu hogar esté protegido en todo momento.
          </p>
        </div>

        <button className="px-4 mt-7 w-full bg-[#7678ed] rounded-lg font-semibold text-white py-2 hover:bg-[#585aff] transition ease-in-out duration-300 ">
          Conoce mas
        </button>
      </div>
      <div className="border border-slate-200 rounded w-full mb-5 lg:mb-0 sm:w-[calc(50%-10px)] lg:w-3/12 p-4 lg:p-8 flex flex-col justify-between">
        <div>
          <div className="text-center text-3xl mb-8 text-[#7678ed]">
            <FontAwesomeIcon icon={faUserNurse} />
          </div>
          <h2 className="text-center mb-6 font-semibold  text-lg">Salud</h2>
          <p className="text-center">
            Protege tu salud con nuestras pólizas de seguros. Ofrecemos
            cobertura integral para garantizar tu bienestar en todo momento.
            Desde consultas médicas hasta tratamientos especializados, estamos
            aquí para cuidar de ti y tu familia
          </p>
        </div>

        <button className="mt-7 px-4 w-full bg-[#7678ed] rounded-lg font-semibold text-white py-2 hover:bg-[#585aff] transition  ease-in-out duration-300 ">
          Conoce mas
        </button>
      </div>
      <div className="border border-slate-200 rounded w-full mb-5 lg:mb-0 sm:w-[calc(50%-10px)] lg:w-3/12 p-4 lg:p-8 flex flex-col justify-between">
        <div className="text-center text-3xl mb-8 text-[#7678ed]">
          <FontAwesomeIcon icon={faIndustry} />
        </div>
        <h2 className="text-center mb-6 font-semibold  text-lg">Empresas</h2>
        <p className="text-center">
          Protege tu empresa con nosotros. Ofrecemos soluciones de seguros
          diseñadas específicamente para las necesidades de tu negocio. Desde
          protección de activos hasta cobertura de responsabilidad.
        </p>

        <button className="mt-7 px-4 w-full bg-[#7678ed] rounded-lg font-semibold text-white py-2 hover:bg-[#585aff] transition ease-in-out duration-300">
          Conoce mas
        </button>
      </div>
    </div>
  );
}

export default Services;
