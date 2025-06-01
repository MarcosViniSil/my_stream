import { useState } from 'react';
import VideoUpload from './pages/upload/videoUpload'

import './App.css';

function App() {
  const [count, setCount] = useState(0);

  return (
    <>
      <VideoUpload/>
    </>
  );
}

export default App;