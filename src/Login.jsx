import React, { useState, useRef } from 'react';
import io from 'socket.io-client';
import Game from './Game';
import './Login.css';
import './App.css';

const socket = io();

function Login() {
  const [showLogin, setShowLogin] = useState(true);
  const [username, setUsername] = useState(null);
  const userNameRef = useRef(null);

  function onLogin() {
    setShowLogin((prevShowLogin) => {
      const userText = userNameRef.current.value;
      setUsername(userText);
      socket.emit('user', { username: userText });
      return !prevShowLogin;
    });
  }

  return (
    <>
      {showLogin === true ? (
        <div className="login">
          <div>
            <h3> Enter Username </h3>
            <input ref={userNameRef} type="text" />
            <button type="submit" onClick={() => onLogin()}>
              Login
            </button>
          </div>
        </div>
      ) : null}
      <Game username={username} />
    </>
  );
}
// <Board spectList={spectList} usernameRef={usernameRef}/>
export default Login;
