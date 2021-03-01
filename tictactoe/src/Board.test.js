import React from 'react';
import './Board.css';
import { useState, useEffect } from 'react';
import io from 'socket.io-client';

const socket = io(); // Connects to socket connection

function calculateWinner()

function Board({spectList, usernameRef}){
    const [board, setBoard] = useState(Array(9).fill(null));
    const [nextX, setNextX] = useState(true);
    const [isSpect, setIsSpect] = useState(false);
    
    

    function handleBoxClick(e, index){
        for(var i = 0; i < spectList.length; i++){
            if(spectList.includes(usernameRef)){
                setIsSpect(true);
            }
        }
        if (isSpect === true){
            e.stopPropagation();
        }else{
            e.preventDefault();
            socket.emit('board', { message: "Player clicked box " + index, index: index }); 
        }
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
                <button onClick={ handleClear }> Reset </button>
            </div>
        </div>
        );
}

export default Board;
