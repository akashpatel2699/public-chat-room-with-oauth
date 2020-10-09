import React from 'react';

const ShowUsers = ({ usersConnected }) => {
    return (
         
        <ul>
            { usersConnected && usersConnected.map((user,index) => <li key={index}>{user}</li>)}
        </ul>
        
    );
}

export default ShowUsers;