import React from 'react';
import './App.css';
import AuthForm from './components/Auth/AuthForm';

function App() {
  return (
    <div className="App bg-gray-100 min-h-screen">
      <header className="App-header">
        <h1>Socket-Hub</h1>
        <p>real time chats with WebSockets</p>
      </header>
      <main>
        <AuthForm />
      </main>
    </div>
  );
}

export default App;
