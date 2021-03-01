import React from 'react';
import Square from './Square.js';
import './Board.css';

const Board = ({ squares, onClick, isSpect }) => (
        <div className='board'>
            {squares.map((square,i) => (
                <Square value={square} onClick={(e) => onClick(e, i)}/>
            ))}
        </div>
    );

export default Board;