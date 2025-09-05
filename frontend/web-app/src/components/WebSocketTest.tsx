import React, { useState, useEffect, useRef } from 'react';
import './WebSocketTest.css';
import { MessageRequest, MessageResponse} from '../types/websocket';
interface Message {
  id: string;
  text: string;
  type: 'sent' | 'received' | 'system';
  timestamp: Date;
}
type WebSocketTestParams ={
  username: string;
};


const WebSocketTest: React.FC <WebSocketTestParams> = ({username} ) => {
  const [messages, setMessages] = useState<Message[]>([]);
  const [inputMessage, setInputMessage] = useState('');
  const [isConnected, setIsConnected] = useState(false);
  const [userId, setUserId] = useState('testuser');
  const [roomId, setRoomId] = useState<string>('');
  const [currentRoom, setCurrentRoom] = useState<string>('');
  const [availableRooms, setAvailableRooms] = useState<string>('');
  const [roomUsers, setroomUsers] = useState<string>('');
  const wsRef = useRef<WebSocket | null>(null);

  const addMessage = (text: string, type: 'sent' | 'received' | 'system') => {
    const newMessage: Message = {
      id: Date.now().toString(),
      text,
      type,
      timestamp: new Date(),
    };
    setMessages(prev => [...prev, newMessage]);
  };

  const connect = () => {
    if (wsRef.current?.readyState === WebSocket.OPEN) {
      addMessage('You are connected', 'system');
      return;
    }

    try {
      const ws = new WebSocket(`ws://localhost:8000/ws/${userId}`);
      wsRef.current = ws;

      ws.onopen = () => {
        setIsConnected(true);
        addMessage('Connected to websocket', 'system');
      };

      ws.onmessage = (event) => {
        addMessage(event.data, 'received');
      };

      ws.onclose = () => {
        setIsConnected(false);
        addMessage('Disconnected from websocket', 'system');
      };

      ws.onerror = (error) => {
        addMessage('Error in websocket connection', 'system');
        console.error('WebSocket error:', error);
      };
    } catch (error) {
      addMessage('Error on connecting', 'system');
      console.error('Connection error:', error);
    }
  };

  const disconnect = () => {
    if (wsRef.current) {
      wsRef.current.close();
      wsRef.current = null;
    }
  };

  const sendMessage = () => {
    if (!inputMessage.trim() || !currentRoom) return;
    
    if (wsRef.current?.readyState === WebSocket.OPEN) {
      const message : MessageRequest = {
        type: 'message',
        content: inputMessage,
        room_id: currentRoom,
        user_id: userId,
        timestamp: new Date().toISOString()
      };
      wsRef.current.send(JSON.stringify(message));
      addMessage(inputMessage, 'sent');
      setInputMessage('');
    } else {
      addMessage('No estás conectado', 'system');
    }
  };
  
  const joinRoom = () => {
      if (!isConnected || !roomId.trim()){
        addMessage('You must be connected and specify a room', 'system');
        return;
      }
      const message: MessageRequest = {
        type: 'join_room',
        content: `Joining room ${roomId}`,
        room_id: roomId,
        user_id: userId,
        timestamp: new Date().toISOString()
      };

      if (wsRef.current?.readyState === WebSocket.OPEN) {
        wsRef.current.send(JSON.stringify(message));

        setCurrentRoom(roomId);
        addMessage(`You joined room: ${roomId}`, 'system');
      }
      else {
        addMessage('You are not connected', 'system');
      }
  }
  const leaveRoom = () => {
    if (!isConnected || !currentRoom) {
      addMessage("You are not in any room", "system");
      return;
    }

    const message: MessageRequest = {
      type: "leave_room",
      content: `leaving room ${roomId}`,
      room_id: roomId,
      user_id: userId,
      timestamp: new Date().toISOString()
    }
    if  (wsRef.current?.readyState === WebSocket.OPEN) {
      wsRef.current.send(JSON.stringify(message));
      setCurrentRoom('');
      addMessage(`You left the room: ${currentRoom}`, 'system');
    }
  };

  const handleKeyPress = (e: React.KeyboardEvent) => {
    if (e.key === 'Enter') {
      sendMessage();
    }
  };

  useEffect(() => {
    // Cleanup on unmount
    return () => {
      if (wsRef.current) {
        wsRef.current.close();
      }
    };
  }, []);

  return (
    <div className="websocket-test">
      <h2>WebSocket Test - Socket-Hub</h2>
      
      <div className="connection-controls">
        <input
          type="text"
          value={userId}
          onChange={(e) => setUserId(e.target.value)}
          placeholder="User ID"
          disabled={isConnected}
        />
        <button onClick={connect} disabled={isConnected}>
          Connect
        </button>
        <button onClick={disconnect} disabled={!isConnected}>
          Disconnect
        </button>
        <span className={`status ${isConnected ? 'connected' : 'disconnected'}`}>
          {isConnected ? '🟢 Connected' : '🔴 Disconnected'}
        </span>
      </div>
      <div className="room-controls">
        <input 
        type="text"
        value={roomId}
        onChange={(e)=>setRoomId(e.target.value)}
        placeholder= "Room ID"
        disabled={!isConnected}
        />
        <button onClick={joinRoom} disabled={!isConnected}>
          Join room
        </button>
        {currentRoom && (
          <>
          <span className="current-room">
            actual room: {currentRoom}
          </span>
          <button onClick={leaveRoom} disabled={!isConnected}>
            Leave room
          </button>
          </>
        )}

      </div>
        
      <div className="message-input">
        <input
          type="text"
          value={inputMessage}
          onChange={(e) => setInputMessage(e.target.value)}
          onKeyDown={handleKeyPress}
          placeholder={currentRoom ? `Message for ${currentRoom}... ` : "Join a room first"}
          disabled={!isConnected || !currentRoom}
        />
        <button onClick={sendMessage} disabled={!isConnected || !currentRoom}>
          Send
        </button>
      </div>

      <div className="messages">
        <h3>Messages:</h3>
        <div className="message-list">
          {messages.map((message) => (
            <div key={message.id} className={`message ${message.type}`}>
              <span className="timestamp">
                {message.timestamp.toLocaleTimeString()}
              </span>
              <span className="text">{message.text}</span>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
};

export default WebSocketTest;
