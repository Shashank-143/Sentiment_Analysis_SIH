import { FeaturesSectionDemo } from "./components/feature";
import { Navbar } from "./components/navbar";
import { DivOrigami } from "./components/animated-logo";
import FeatureGrid from "./components/three-cards";
import { ThreeDMarqueeDemoSecond } from "./components/3-dmarquee/3-d-marquee-main";
import AccordionDemo from "./components/accordion";
import Footer from "./components/footer";
import { GaugeDemo } from "./components/gauge";


export default function Home() {
  return (
    <>
      <Navbar />
      <ThreeDMarqueeDemoSecond />
      <GaugeDemo />
      <DivOrigami />
      <FeatureGrid />
      <FeaturesSectionDemo />
      <AccordionDemo />
      <Footer />
    </>
  );
}
