import React from 'react';

const ShowUsers = ({ usersConnected }) => {
    return (
        <div className="users-container">
            <h3>ONLINE</h3>
            <div className="position-list">
                <ul className="users-list">
                    { usersConnected && usersConnected.map((user,index) => <li key={index}>{user}</li>)}
                </ul>
            </div>
        </div>
        
    );
}

export default ShowUsers;