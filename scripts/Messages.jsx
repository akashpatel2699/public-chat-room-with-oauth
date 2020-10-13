import React from 'react';
import Message from './Message';

const Messages = ({messages, username}) => {
    return (
    //   {messages.map( (message) => <Message message={message} />)}
        <div className="messages-container">
            { messages && messages.map( (message,index) => <Message username={username} key={index} message={message} />)}
        </div>
    );
}

export default Messages;