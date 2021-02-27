import './App.css';
import Board from './Board.js';
import { useState, useRef, useEffect } from 'react';
import io from 'socket.io-client';

const socket = io(); // Connects to socket connection


function App() {
  const [showLogin, setShowLogin] = useState(true);
  const usernameRef = useRef(null);
  const [playerX, setPlayerX] = useState(null);
  const [playerO, setPlayerO] = useState(null);
  const [spectList, setSpectList] = useState([]);
  
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
      setPlayerX(data.playerX);
      setPlayerO(data.playerO);
      const newSpectList = data.spectators;
      setSpectList(spectList.push(...newSpectList));
    });
  }, [playerX, playerO]);
  
  
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
        <h1> Player X: { playerX }</h1>
        <h1> Player O: { playerO }</h1>
      </div>
      <div>
        <Board />
      </div>
      <div><button> Reset </button></div>
      <div>
        {spectList}
      </div>
    </div>
  );
}

export default App;
