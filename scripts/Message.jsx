import React, { useEffect, useState } from 'react';
import ReactHtmlParser from 'react-html-parser';

const Message = ({ message, username}) => {
    
    const [style, setStyle ] = useState("message")
    
    useEffect(() => {
        (username === message['username'])? setStyle(prev => prev + " right-side"): null;
        ("sugerBot" === message['username']) ? setStyle( prev => prev + " bot-message"): null;
    },[]) 
    
    let string_datetime_object = string => new Date(Date.parse(string));
    let created_at = string_datetime_object(message['created_at']);
        
    const imageOrAnchorTag = (url) => {
        let html_tag = "";
        if (url.message_type === "image url"){
            html_tag = `<a href=${url.message} target="_blank">${url.message}</a><br>
                <img src=${url.message}>`;
        }else {
            html_tag = `<a href=${url.message} target="_blank">${url.message}</a>`;
        }

        return html_tag
    }
    
    return (
        <div className={style}>
            <p className="username">
                <strong>
                    {message['username']}
                </strong>
                <span>
                    {created_at.getMonth()}/
                    {created_at.getDay()}/
                    {created_at.getFullYear()} 
                    {
                        created_at.getHours() === 12? created_at.getHours(): 
                        created_at.getHours() % 12}:{created_at.getMinutes()
                    }
                </span>
            </p>
            <p className="main-message">
                    { ReactHtmlParser(
                       ( message.message_type === "url link" || message.message_type === "image url" )?
                        imageOrAnchorTag(message) : message.message
                    ) }
            </p>
        </div>
    );
}

export default Message;