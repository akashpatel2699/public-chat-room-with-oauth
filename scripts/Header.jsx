import React from 'react';

const Header = ({ username}) => {
    return (
        <h1 
            className="header">
            Welcome {username} to the public chat room
        </h1>    
    );
}

export default Header;