import React, { useState, useEffect } from 'react';
import Board from './Board.js';
import { calculateWinner } from './helpers.js';
import io from 'socket.io-client';
import './Game.css';

const socket = io();

const styles = {
    width: '200px',
    margin: '20px auto'
}

function Game({username}) {
    const[board, setBoard] = useState(Array(9).fill(null));
    const[xNext, setXNext] = useState(true);
    const[playerX, setPlayerX] = useState(null);
    const[playerO, setPlayerO] = useState(null);
    const[spectList, setSpectList] = useState([]);
    const winner = calculateWinner(board);
    
    function handleBoxClick(e, index){
        if(xNext && playerX == username){
            socket.emit('board', { message: "Player clicked box " + index, index: index});
        } else if (!xNext && playerO == username){
            socket.emit('board', { message: "Player clicked box " + index, index: index});
        } else if(isSpect(username)){
            return null;
        }
    }
    
    function handleClear(){
        setBoard(Array(9).fill(null));
        setXNext(true);
        socket.emit('reset', { message: "Reset/Play Again was clicked" });
    }
    
    function isSpect(user){
        return spectList.includes(username);
    }
    
    useEffect(() => {
        socket.on('board', data => {
            console.log('Board was clicked!');
            console.log(data);
            const newBoard = [...board];
            if (winner || newBoard[data.index]) return;
            newBoard[data.index] = xNext ? 'X' : 'O';
            setBoard(newBoard);
            setXNext(!xNext);
        })
    }, [board, xNext, winner])
    
        
    useEffect(() => {     
        socket.on('reset', data => {
            console.log('Resetting game');
            console.log(data);
            setBoard(Array(9).fill(null));
            setXNext(true);
        })
    }, [])
    
    useEffect(() => { 
        socket.on('playerX', data => {
            setPlayerX(data.playerX);
        });
    }, [playerX])
    
    useEffect(() => { 
        socket.on('playerO', data => {
            setPlayerO(data.playerO);
        });
    }, [playerO])
    
    useEffect(() => { 
        socket.on('spectators', data => {
            const arr = data.spectators;
            setSpectList(arr);
        });
    }, [spectList])
    
    return (
        <div className='container'>
            <h1> Welcome {username} </h1>
            <Board squares={ board } onClick={ handleBoxClick } username={username}/>
            <div style={ styles }>
                <p> Player X : { playerX } </p>
                <p> Player O : { playerO } </p>
                <p>{ winner ? 'Winner: ' + winner : 'Next Player: ' + (xNext ? 'X' : 'O')}</p>
                { !isSpect(username) ?
                <p>{ winner ? <button onClick={ handleClear }> Play Again </button> : <button onClick={ handleClear }> Reset </button> }</p> : null }
                <p> Spectators:</p>
                { spectList.map((user, i) => ( <p> { user } </p> )) }
            </div>
        </div>
    )
}

export default Game;