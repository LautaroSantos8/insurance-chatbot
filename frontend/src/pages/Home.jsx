import React from "react";
import HomeHeader from "../components/homeHeader/HomeHeader";
import Slider from "../components/slider/Slider";
import Services from "../components/services/Services";
import Tabs from "../components/tabs/Tabs";
import Footer from "../components/footer/Footer";
import Articles from "../components/articles/Articles";

function Home() {
  return (
    <div>
      <HomeHeader />
      <Slider />
      <div className="px-8 max-w-7xl mx-auto">
        <Services />
        <Tabs />
        <Articles />
      </div>
      <Footer />
    </div>
  );
}

export default Home;
