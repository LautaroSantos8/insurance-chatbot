import React from "react";

function Articles() {
  return (
    <div className="pb-20">
      <h2 className="font-semibold text-2xl pt-12 text-center  mb-24">
        Articulos
      </h2>

      <div className="flex flex-wrap lg:flex-nowrap md:gap-5 mt-20 justify-between">
        <div className="w-full md:w-[calc(50%-10px)] lg:w-4/12">
          <img
            className="w-full rounded-lg shadow-sm"
            src="./article1.png"
            alt=""
          />
          <div className="mt-4 mb-8">
            <h2 className="font-semibold mb-4">
              ¿Como adquirir tu seguro en linea?
            </h2>
            <div className="text-justify">
              Descubre cómo comprar un seguro en línea de manera rápida y
              segura. En este artículo, exploraremos los pasos clave para
              seleccionar y adquirir la mejor cobertura para tus necesidades...
              <button className="text-[#7678ed] font-semibold pl-2">
                Ver mas
              </button>
            </div>
          </div>
        </div>
        <div className="w-full md:w-[calc(50%-10px)] lg:w-4/12">
          <img
            className="w-full rounded-lg shadow-sm"
            src="./article2.png"
            alt=""
          />
          <div className="mt-4 mb-8">
            <h2 className="font-semibold mb-4">
              ¿Qué cubre el seguro todo riesgo?
            </h2>
            <div className="text-justify">
              Explora la cobertura completa del seguro todo riesgo. Descubre
              cómo esta póliza ofrece protección contra una amplia gama de
              riesgos, desde accidentes automovilísticos hasta daños...
              <button className="text-[#7678ed] font-semibold pl-2">
                Ver mas
              </button>
            </div>
          </div>
        </div>
        <div className="w-full md:w-[calc(50%-10px)] lg:w-4/12">
          <img
            className="w-full rounded-lg shadow-sm"
            src="./article3.png"
            alt=""
          />
          <div className="mt-4">
            <h2 className="font-semibold mb-4">
              Chatbot: Encuentra tu Seguro Ideal
            </h2>
            <div className="text-justify">
              Con nuestro chatbot, encontrar el seguro perfecto es fácil y
              rápido. Conversa con nosotros y descubre las opciones diseñadas
              para cubrir tus necesidades específicas...
              <button className="text-[#7678ed] font-semibold pl-2">
                Ver mas
              </button>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}

export default Articles;
