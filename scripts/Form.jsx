import React, { useState } from 'react';
import PropTypes from 'prop-types';
import Socket from './Socket';

const Form = ({ email }) => {
  const [input, setInput] = useState('');
  const [buttonState, setButtonState] = useState(true);

  const handleChange = (event) => {
    const data = event.target.value;
    if (data.trim().length > 0) {
      setButtonState(false);
    } else {
      setButtonState(true);
    }
    setInput(data);
  };
  const handleClick = (e) => {
    e.preventDefault();
    setInput('');
    setButtonState(true);
    Socket.emit('new message', {
      chat: input,
      email,
    });
  };

  return (
    <form className="text-input">
      <input
        value={input}
        type="text"
        onChange={handleChange}
        className="user-input"
        required
      />
      <button
        type="submit"
        id="button"
        onClick={handleClick}
        disabled={buttonState}
      >
        Submit
      </button>
    </form>
  );
};

Form.propTypes = {
  email: PropTypes.string,
};
Form.defaultProps = {
  email: '',
};

export default Form;
