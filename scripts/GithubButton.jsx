import React from 'react';
import GitHubLogin from 'react-github-login';
import Socket from './Socket';

const onSuccess = (response) => {
  Socket.emit('new github user', { code: response.code });
};
/* eslint-disable no-console */
const onFailure = (response) => console.error(response);
/* eslint-enable no-console */

const GithubButton = () => (
  <GitHubLogin
    clientId="Iv1.6393fa29ac6d0900"
    redirectUri=""
    onSuccess={onSuccess}
    onFailure={onFailure}
  />
);

export default GithubButton;
