import './App.css';
import Board from './Board.js';
import { useState, useRef, useEffect } from 'react';
import io from 'socket.io-client';

const socket = io(); // Connects to socket connection


function App() {
  const [showLogin, setShowLogin] = useState(true);
  const usernameRef = useRef(null);
  
  function onLogin() {
    setShowLogin((prevShowLogin) => {
      const userText = usernameRef.current.value;
      socket.emit('user', { username: userText });
      console.log('User logged in');
      return !prevShowLogin;
    });
  }
  
  useEffect(() => {
    socket.on('user', (data) => {
      console.log('Login even received!');
      console.log(data);
    });
  }, []);
  
  
  return (
    <div className="App">
      <h1 className="title"> Tic Tac Toe ! </h1>
      {showLogin === true ?
      <div className='login'>
        <div>
          <h3> Enter Username </h3>
          <input ref={usernameRef} type="text"></input>
          <button onClick={() => onLogin()}>Login</button>
        </div>
      </div> : null }
      <div>
        <Board />
      </div>
      <div><button> Reset </button></div>
    </div>
  );
}

export default App;
