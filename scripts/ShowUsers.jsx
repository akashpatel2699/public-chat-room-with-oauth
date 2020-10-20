import React, { Fragment } from 'react';

const ShowUsers = ({ usersConnected }) => {
    return (
        <div className="users-container">
            <h3>ONLINE {usersConnected.length}</h3>
            <div className="position-list">
                <ul className="users-list">
                    { usersConnected[0] && usersConnected.map((user,index) => 
                        <li key={index}>
                            <div>
                                <div>
                                    <img src={user.profile_url} alt="User Profile"/>
                                </div>
                                <div>
                                    {user.username} {user.auth_type}
                                </div>
                            </div>
                        </li>
                    )}
                </ul>
            </div>
        </div>
        
    );
}

export default ShowUsers;