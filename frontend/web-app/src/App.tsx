import React, {useState, useEffect} from 'react';
import './App.css';
import AuthForm from './components/Auth/AuthForm';
import WebSocketTest from './components/WebSocketTest';

function App() {
  const [isLoggedin, setIsLoggedin] = useState(false);
  const [username, setUsername] = useState('');

  const checkAuthStatus = async () => {
    const token = localStorage.getItem('token');
    if (token) {
      try {
        const response = await fetch('/api/auth/me', {
          headers: {
            'Authorization': `Bearer ${token}`
          }
        });
        
        if (response.ok) {
          const userData = await response.json();
          setUsername(userData.sub || '');
          setIsLoggedin(true);
        } else {
          // Token is invalid, remove it
          localStorage.removeItem('token');
          setIsLoggedin(false);
          setUsername('');
        }
      } catch (error) {
        console.error('Auth check failed:', error);
        localStorage.removeItem('token');
        setIsLoggedin(false);
        setUsername('');
      }
    }
  };

  useEffect(() => {
    checkAuthStatus();
  }, []);

  const handleLogout = () => {
    localStorage.removeItem('token');
    setIsLoggedin(false);
    setUsername('');
  };

  return (
    <div className="App bg-gray-100 min-h-screen">
      <header className="App-header">
        <h1>Socket-Hub</h1>
        <p>real time chats with WebSockets</p>
        {isLoggedin && (
          <div className="user-info">
            <span>Welcome, {username}!</span>
            <button 
              onClick={handleLogout}
              className="ml-4 px-4 py-2 bg-red-500 text-white rounded hover:bg-red-600"
            >
              Logout
            </button>
          </div>
        )}
      </header>
      <main>
        {isLoggedin ? <WebSocketTest username={username} /> : <AuthForm setIsLoggedin={setIsLoggedin} setUsername={setUsername}/> }
      </main>
    </div>
  );
}

export default App;
