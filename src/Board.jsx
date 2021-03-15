import React from 'react';
import PropTypes from 'prop-types';
import Square from './Square';
import './Board.css';

const Board = ({ squares, onClick, isSpect }) => (
  <div className="board">
    {squares.map((square, i) => (
      <Square value={square} onClick={(e) => onClick(e, i)} />
    ))}
  </div>
);

Board.propTypes = {
  squares: PropTypes.string.isRequired,
  onClick: PropTypes.func.isRequired,
  isSpect: PropTypes.func.isRequired,
};

export default Board;
