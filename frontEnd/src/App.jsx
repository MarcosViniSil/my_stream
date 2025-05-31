import { useState } from 'react';
import MenuResponsive from './layout/menuReponsive/MenuReponsive'

import './App.css';

function App() {
  const [count, setCount] = useState(0);

  return (
    <>
      <MenuResponsive/>
    </>
  );
}

export default App;