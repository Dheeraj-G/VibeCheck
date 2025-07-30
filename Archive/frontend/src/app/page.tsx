import Image from "next/image";
import '../../framer/styles.css'

import HomeBodyFramerComponent from '../../framer/home-body'
import BackgroundFramerComponent from '../../framer/background'

export default function Home() {
  return (
    <div className='flex flex-col items-center gap-3 bg-[rgb(0,_0, 0)]'>
      <HomeBodyFramerComponent.Responsive/>
      <BackgroundFramerComponent.Responsive/>
    </div>
  );
}
