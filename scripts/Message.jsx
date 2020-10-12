import React, { Fragment } from 'react';

const Message = ({ message}) => {
    return (
        <Fragment>
            <p>{message['username']}  {message['created_at']}</p>
            <p>{message['message']}</p> 
        </Fragment>
    );
}

export default Message;