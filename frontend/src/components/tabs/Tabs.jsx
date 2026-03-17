import React, { useState, useEffect, useRef, useLayoutEffect } from "react";

function Tabs() {
  const [underline, setUnderline] = useState(true);
  const [tabs, setTabs] = useState([]);
  const [btns, setBtns] = useState([]);

  useEffect(() => {
    const tab = document.getElementsByClassName("tab");
    setTabs(tab);
    const btn = document.getElementsByClassName("btn");
    setBtns(btn);
  }, []);

  tabs[0]?.classList?.remove("hidden");
  btns[0]?.classList.add("border-b-4", "border-[#7678ed]");

  const handleTab = (e) => {
    for (let i = 0; i < tabs.length; i++) {
      if (tabs[i].getAttribute("name") === e.target.id) {
        tabs[i].classList.remove("hidden");
        btns[i].classList.add("border-b-4", "border-[#7678ed]");
      } else {
        tabs[i].classList.add("hidden");
        btns[i].classList.remove("border-b-4");
      }
    }
  };

  return (
    <div className="mt-28">
      <div className="flex justify-center mb-28">
        <ul className="flex text-lg sm:text-xl">
          <li className=" font-semibold mr-4 px-2 btn pb-3">
            <button id="1" onClick={handleTab}>
              Nosotros
            </button>
          </li>
          <li className="font-semibold mr-4 px-2 btn pb-3">
            <button id="2" onClick={handleTab}>
              {" "}
              Responsabilidades
            </button>
          </li>
          <li className="font-semibold btn px-2 pb-3">
            <button id="3" onClick={handleTab}>
              Beneficios
            </button>
          </li>
        </ul>
      </div>
      <div className="flex flex-wrap mb-8 tab hidden" name="1">
        <div className="w-full md:w-5/12">
          <img src="./tab1.png" alt="" className="rounded-lg shdow-sm" />
        </div>
        <div className="w-full md:w-7/12 lg:p-8 md:pl-8 flex items-center tab1 mt-8 md:mt-0">
          <div>
            <h2 className="font-semibold mb-6 text-xl">¿Quienes somos?</h2>
            <p>
              Nos dedicamos a proteger lo que más valoras. Con un equipo de
              expertos en seguros, brindamos soluciones personalizadas y
              confiables para garantizar tu tranquilidad. Nuestra misión es
              estar a tu lado en cada paso del camino, ofreciéndote la seguridad
              y la tranquilidad que mereces. Descubre cómo podemos proteger lo
              que más importa para ti y tu familia.
            </p>
            <p className="mt-2">
              Con años de experiencia y un enfoque centrado en el cliente, nos
              esforzamos por ofrecerte la mejor cobertura y atención
              personalizada. Tu tranquilidad es nuestra prioridad absoluta.
            </p>
          </div>
        </div>
      </div>
      <div className="flex flex-wrap mb-8 tab hidden" name="2">
        <div className="w-full md:w-5/12">
          <img src="./tab2.png" alt="" className="rounded-lg shdow-sm" />
        </div>
        <div className="w-full md:w-7/12 lg:p-8 md:pl-8 flex items-center tab1 mt-8 md:mt-0">
          <div>
            <h2 className="font-semibold mb-6 text-xl">
              Protegiendo lo que más importa: Tu seguridad y tranquilidad
            </h2>
            <p>
              Asumimos la responsabilidad de proteger tus intereses y bienes.
              Nos comprometemos a brindarte pólizas de seguros confiables y
              transparentes que te protejan en todo momento. Nuestro objetivo es
              garantizar que recibas la atención y el apoyo necesarios cuando
              más lo necesites, para que puedas enfrentar cualquier eventualidad
              con confianza y tranquilidad
            </p>
          </div>
        </div>
      </div>
      <div className="flex flex-wrap mb-8 tab hidden" name="3">
        <div className="w-full md:w-5/12">
          <img src="./tab3.png" alt="" className="rounded-lg shdow-sm" />
        </div>
        <div className="w-full md:w-7/12 lg:p-8 md:pl-8 flex items-center tab1 mt-8 md:mt-0">
          <div>
            <h2 className="font-semibold mb-6 text-xl">
              Ventajas Exclusivas para Tu Protección y Tranquilidad
            </h2>
            <p>
              Descubre los beneficios de elegir nuestra empresa para proteger lo
              que más valoras. Desde cobertura integral hasta atención
              personalizada, te ofrecemos una amplia gama de ventajas diseñadas
              para brindarte seguridad y tranquilidad. Con nosotros, puedes
              estar seguro de recibir el respaldo que necesitas en cada paso del
              camino
            </p>
            <p className="mt-2">
              te ofrecemos asesoramiento experto y un proceso de reclamación
              ágil y sin complicaciones. Nuestro compromiso es brindarte
              tranquilidad y respaldo en cada situación, para que puedas vivir
              con confianza y seguridad en tu día a día
            </p>
          </div>
        </div>
      </div>
    </div>
  );
}

export default Tabs;
