import React from 'react';

const ShowUsers = ({ usersConnected }) => {
    return (
        <div className="users-container">
            <h3>ONLINE {usersConnected.length}</h3>
            <div className="position-list">
                <ul className="users-list">
                    { usersConnected[0] && usersConnected.map((user,index) => <li key={index}>{user.username} {user.auth_type}</li>)}
                </ul>
            </div>
        </div>
        
    );
}

export default ShowUsers;