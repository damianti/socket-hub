import React from 'react';
import './App.css';
import WebSocketTest from './components/WebSocketTest';

function App() {
  return (
    <div className="App">
      <header className="App-header">
        <h1>Socket-Hub</h1>
        <p>real time chats with WebSockets</p>
      </header>
      <main>
        <WebSocketTest />
      </main>
    </div>
  );
}

export default App;
