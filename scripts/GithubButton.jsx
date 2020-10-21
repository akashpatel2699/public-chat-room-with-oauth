import React from 'react';
import ReactDOM from 'react-dom';
import GitHubLogin from 'react-github-login';
import { Socket } from './Socket';
 
const onSuccess = response => {
    Socket.emit('new github user', {'code': response.code})
}
const onFailure = response => console.error(response);
 
export const GithubButton = () => {
    return (
      <GitHubLogin 
        clientId="Iv1.225a6103dab2fcc6"
        redirectUri=""
        onSuccess={onSuccess}
        onFailure={onFailure}
       />
    );
}