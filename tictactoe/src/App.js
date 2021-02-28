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
  // has side effect; multiple login events
  useEffect(() => {
    socket.on('user', (data) => {
      console.log('Login event received!');
      if(playerX === null){
        setPlayerX(data.playerX);
        console.log(data);
      }
      if(playerO === null){
        setPlayerO(data.playerO);
        console.log(data);
      }
      if(data.spectators) {
        const newSpectList = data.spectators;
        const newList = [...spectList];
        newList.splice(0, newList.length, ...newSpectList);
        setSpectList(newList);
      }
    });
  }, [playerX, playerO, spectList]);
  
  
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
        <Board spectList={spectList} usernameRef={usernameRef}/>
      </div>
    </div>
  );
}

export default App;
