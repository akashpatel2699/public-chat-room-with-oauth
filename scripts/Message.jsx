import React, {Fragment } from 'react';

const string_datetime_object = string => new Date(Date.parse(string));

const Message = ({ message }) => {
    let created_at = string_datetime_object(message['created_at'])
    
    return (
        <Fragment>
            <p>{message['username']}=>{created_at.getHours() === 12? created_at.getHours(): created_at.getHours() % 12}:{created_at.getMinutes()}</p>
            <p>{message['message']}</p> 
        </Fragment>
    );
}

export default Message;