import React from 'react';
import Message from './Message';

const Messages = ({messages}) => {
    return (
    //   {messages.map( (message) => <Message message={message} />)}
        <div>
            { messages && messages.map( (message,index) => <Message key={index} message={message} />)}
        </div>
    );
}

export default Messages;