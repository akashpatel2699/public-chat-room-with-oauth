import React , { useEffect, useRef }from 'react';
import Message from './Message';


const Messages = ({messages, username}) => {
    
    const messagesEndRef = useRef(null)
    
    const scrollToBottom = () => {
        messagesEndRef.current.scrollIntoView({ behavior: "smooth" })
    }

    useEffect(scrollToBottom, [messages]);
    
    return (
        <div className="messages-container">
            { messages &&
                messages.map( (message,index) => <Message username={username} key={index} message={message} />
            )}
            <div ref={messagesEndRef} />
        </div>
    );
}

export default Messages;