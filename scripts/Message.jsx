import React, { useEffect, useState } from 'react';

const string_datetime_object = string => new Date(Date.parse(string));

const Message = ({ message, username }) => {
    const [style, setStyle ] = useState("message")
    
    useEffect(() => {
        username === message['username']? setStyle(prev => prev + " right-side"): null;
        // message['username'] === 'sugarBot'? setStyle(prev => prev + " bot-message"): null;
        "sugerBot" === message['username'] ? setStyle( prev => prev + " bot-message"): null;
    },[]) 
    
    let created_at = string_datetime_object(message['created_at'])
    // let style = username === message['username']? "message right-side" : "message";
    // { message['username'] === 'sugarBot' && style.concat(" bot-message")}
    
    return (
        <div className={style}>
            <p className="username"><strong>{message['username']}</strong>
            <span>{created_at.getHours() === 12? created_at.getHours(): 
                created_at.getHours() % 12}:{created_at.getMinutes()}</span></p>
            <p>{message['message']}</p>
        </div>
    );
}

export default Message;