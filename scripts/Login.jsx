import React from 'react';
import { FacebookButton } from './FacebookButton';
import { GithubButton } from './GithubButton';
import { GoogleButton } from './GoogleButton';

const Login = ({ setUsername }) => {
    
    return (
        <div>
            <FacebookButton setUsername={setUsername}/>
            <GithubButton />
            <GoogleButton />
        </div>
    );
};

export default Login;