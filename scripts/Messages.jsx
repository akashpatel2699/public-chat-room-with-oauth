import React, { useEffect, useRef } from 'react';
import PropTypes from 'prop-types';
import Message from './Message';

const Messages = ({ messages, username }) => {
  const messagesEndRef = useRef(null);

  const scrollToBottom = () => {
    messagesEndRef.current.scrollIntoView({ behavior: 'smooth' });
  };

  useEffect(scrollToBottom, [messages]);
  return (
    <div className="messages-container">
      { messages
                && messages.map(
                  (message, index) => (
                    <Message
                      username={username}
                      /* eslint-disable */
                      key={index}
                      /* eslint-enable */
                      message={message}
                    />
                  ),
                )}
      <div ref={messagesEndRef} />
    </div>
  );
};

Messages.propTypes = {
  messages: PropTypes.arrayOf(PropTypes.string),
  username: PropTypes.string,
};
Messages.defaultProps = {
  messages: [],
  username: '',
};

export default Messages;
