import React from 'react';
import { FacebookButton } from './FacebookButton';
import { GithubButton } from './GithubButton';
import { GoogleButton } from './GoogleButton';

const Login = ({ setUsername}) => {
    
    return (
        <div className="login-container">
            <div className="login-buttons">
                <FacebookButton setUsername={setUsername}/>
                <GithubButton />
                <GoogleButton />
            </div>
        </div>
    );
};

export default Login;