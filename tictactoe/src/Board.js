import React from 'react';
import './Board.css';
import { useState, useEffect } from 'react';
import io from 'socket.io-client';

const socket = io(); // Connects to socket connection


function Board({spectList, usernameRef}){
    const [board, setBoard] = useState(Array(9).fill(null));
    const [nextX, setNextX] = useState(true);
    const [isSpect, setIsSpect] = useState(false);
    
    

    function handleBoxClick(e, index){
        e.preventDefault();
        for(var i = 0; i < spectList.length; i++){
            if(usernameRef === spectList[i]){
                setIsSpect(true);
            }
        }
        //check if currentUser is in spectList
        //prevention
        socket.emit('board', { message: "Player clicked box " + index, index: index });
    };
    
    function handleClear(){
        setBoard(["","","","","","","","",""]);
        setNextX(true);
    }
    
    useEffect(() => {
        socket.on('board', (data) => {
            console.log('Board was clicked!');
            console.log(data);
            const newBoard = [...board];
            newBoard[data.index] = nextX ? "X" : "O";
            setNextX(!nextX);
            setBoard(newBoard);
        });
    }, [board, nextX]);
    
    return(
        <div>
            <div className="board">
                { board.map((item, i) =>( <div className="box" onClick={ (e) => handleBoxClick(e, i) }> { item } </div> )) }
            </div>
            <div>
                <button onClick={ handleClear } disabled={ isSpect }> Reset </button>
            </div>
        </div>
        );
}

export default Board;
