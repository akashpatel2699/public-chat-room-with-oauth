import React from 'react';
import ReactDOM from 'react-dom';
import { GoogleLogin } from 'react-google-login';
import { Socket } from './Socket';

const onSuccessGoogle = (response) => {
    console.log("success")
    let id_token = response.getAuthResponse().id_token;
    Socket.emit("new google user", {
        'id_token': id_token
    })
}
const onFailureGoogle = (response) => {
    console.log("failure")
    console.log(response)
}
 
export const GoogleButton = () => {
    
    return (
      <GoogleLogin
        clientId="209640983095-i1n972h3s4te5at8bdc0v91dmj89joit.apps.googleusercontent.com"
        buttonText="Login"
        onSuccess={onSuccessGoogle}
        onFailure={onFailureGoogle}
        cookiePolicy={'single_host_origin'}
      />
    );
}