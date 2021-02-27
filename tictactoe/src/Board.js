import React from 'react';
import './Board.css';
import { useState, useEffect } from 'react';
import io from 'socket.io-client';

const socket = io(); // Connects to socket connection


function Board(){
    const [board, setBoard] = useState(Array(9).fill(null));
    const [xNext, setX] = useState(true);
    

    function handleBoxClick(e, index){
        e.preventDefault();
        // const newBoard = [...board];
        // newBoard[index] = xNext ? "X" : "O";
        // setBoard(newBoard);
        // setX(!xNext);
        socket.emit('board', { message: "Player clicked box " + index, index: index });
    };
    
    useEffect(() => {
        socket.on('board', (data) => {
            console.log('Board was clicked!');
            console.log(data);
            const newBoard = [...board];
            newBoard[data.index] = xNext ? "X" : "O";
            setX(!xNext);
            setBoard(newBoard);
        });
    }, [board, xNext]);
    
    return(
        <div className="board">
            { board.map((item, i) =>( <div className="box" onClick={ (e) => handleBoxClick(e, i) }> { item } </div> )) }
        </div>
        );
}

export default Board;
