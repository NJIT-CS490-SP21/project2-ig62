import React from 'react';
import './Board.css';
import { useState, useRef, useEffect } from 'react';
import io from 'socket.io-client';

const socket = io(); // Connects to socket connection


function Board(){
    const [board, setBoard] = useState(["","","","","","","","",""]);
    

    function handleBoxClick(e, index){
        e.preventDefault();
        const newBoard = [...board];
        newBoard[index] = "X";
        setBoard(newBoard);
        socket.emit('board', { message: "Player clicked box " + index, index: index });
    };
    
    useEffect(() => {
        
        socket.on('board', (data) => {
            console.log('Board was clicked!');
            console.log(data);
            const newBoard = [...board];
            newBoard[data.index] = "X";
            setBoard(newBoard);
        });
    }, [board]);
    
    return(
        <div className="board">
            { board.map((item, i) =>( <div className="box" onClick={ (e) => handleBoxClick(e, i) }> { item } </div> )) }
        </div>
        );
}

export default Board;
