import React, {useState} from 'react';
import './App.css';
import AuthForm from './components/Auth/AuthForm';
import WebSocketTest from './components/WebSocketTest';

function App() {
  const [isLoggedin, setIsLoggedin] = useState (false);
  const [username, setUsername] = useState ('');

  return (
    <div className="App bg-gray-100 min-h-screen">
      <header className="App-header">
        <h1>Socket-Hub</h1>
        <p>real time chats with WebSockets</p>
      </header>
      <main>
        {isLoggedin ? <WebSocketTest /> : <AuthForm setIsLoggedin={setIsLoggedin} setUsername={setUsername}/> }
      </main>
    </div>
  );
}

export default App;
