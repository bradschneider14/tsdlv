import React from 'react';
import './App.css';

import SessionComponent from './components/SessionComponent'

function App() {
  return (
    <div className="App">
      <header className="App-header">
        Time Series Data Log Viewer
      </header>

      <div className="Content">
        <SessionComponent />


      </div>
    </div>
  );
}

export default App;
