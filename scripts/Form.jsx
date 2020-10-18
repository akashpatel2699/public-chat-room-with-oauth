import React, { useState } from "react";
import { Socket } from './Socket';

const Form = () => {
  const [input, setInput] = useState("");
  const [buttonState, setButtonState] = useState(true);

  const handleChange = (event) => {
    const data = event.target.value;
    if (data.trim().length > 0) setButtonState(false);
    else setButtonState(true);
    setInput(data);
  };
  const handleClick = (e) => {
    e.preventDefault();
    setInput("");
    setButtonState(true);
    Socket.emit("new message", {
        'chat':input,    
    })
  };

  return (
    <form className="text-input">
      <input value={input} type="text" onChange={handleChange} className="user-input" required />
      <button id="button" onClick={handleClick} disabled={buttonState}>
        Submit
      </button>
    </form>
  );
};

export default Form;
