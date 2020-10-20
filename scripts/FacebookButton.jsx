import React from 'react';
import ReactDOM from 'react-dom';
import FacebookLogin from 'react-facebook-login';
import { Socket } from './Socket';
 
 export const FacebookButton = ({ setUsername }) => {
    
    const responseFacebook = (response) => {
    console.log(response.email)
    Socket.emit("new facebook user", {
      'name': response.name,
      'email': response.email
    })
    setUsername(response.name);
    }
    
    
    return(
      <FacebookLogin
        appId="993947061124717"
        autoLoad={false}
        textButton="Facebook Login"
        fields="name,email,picture"
        callback={responseFacebook} />
    );
 }