import React, { Fragment } from 'react';

const ShowUsers = ({ usersConnected }) => {
    return (
        <div className="users-container">
            <h3>
                ONLINE {usersConnected.length}
            </h3>
            <div className="position-list">
                <ul className="users-list">
                    { usersConnected[0] && 
                        usersConnected.map((user,index) => 
                            <li key={index}>
                                <div className="connected-user">
                                    <div className="connected-user-profile">
                                        <img src={user.profile_url} alt="User Profile"/>
                                    </div>
                                    <div className="connected-user-info">
                                        <span className="connected-user-username"> {user.username}</span> 
                                        <span className="connected-user-auth-type">{user.auth_type}</span>
                                    </div>
                                </div>
                            </li>
                        )
                    }
                </ul>
            </div>
        </div>
        
    );
}

export default ShowUsers;