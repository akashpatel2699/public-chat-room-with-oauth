import React, { useEffect, useState } from 'react';
import ReactHtmlParser from 'react-html-parser';

const Message = ({ message, username}) => {
    const [style, setStyle ] = useState("message")
    
    useEffect(() => {
        username === message['username']? setStyle(prev => prev + " right-side"): null;
        "sugerBot" === message['username'] ? setStyle( prev => prev + " bot-message"): null;
    },[]) 
    let string_datetime_object = string => new Date(Date.parse(string));
    let created_at = string_datetime_object(message['created_at']);
        
    const showImageInline = (img_tag) => {
        let src_starts_at = img_tag.search("src=") + 4;
        let src = img_tag.slice(src_starts_at,img_tag.search("alt")-1);
        return `<a href=${src} target="_blank">${src}</a><br>${img_tag}`
    }
    return (
        <div className={style}>
            <p className="username"><strong>{message['username']}</strong>
            <span>
                {created_at.getMonth()}/
                {created_at.getDay()}/
                {created_at.getFullYear()} {created_at.getHours() === 12? created_at.getHours(): 
                created_at.getHours() % 12}:{created_at.getMinutes()}</span></p>
            <p className="main-message">{ ReactHtmlParser(message['message'].includes("alt='failed to load and image'")? 
            showImageInline(message['message'])  : message['message']) }</p>
        </div>
    );
}

export default Message;