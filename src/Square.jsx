import React from 'react';
import PropTypes from 'prop-types';
import './Square.css';

const Square = ({ value, onClick }) => (
  <button type="button" className="square" onClick={onClick}>
    {value}
  </button>
);

Square.propTypes = {
  value: PropTypes.string.isRequired,
  onClick: PropTypes.func.isRequired,
};
export default Square;
