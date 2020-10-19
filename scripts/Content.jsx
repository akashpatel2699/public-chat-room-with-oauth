    
import * as React from 'react';
import  Form  from './Form';
import { Socket } from './Socket';
import Header from './Header';
import Messages from './Messages';
import ShowUsers from './ShowUsers';
import Login from './Login';

export function Content() {
    const [messages, setMessages] = React.useState([]);
    const [username, setUsername] = React.useState("");
    const [usersConnected, setUsersConnected] = React.useState([]);
    const [userLoggedIn, setUserLoggedIn] = React.useState(false);
    
    function getNewAddresses() {
        React.useEffect(() => {
            Socket.on('joinuser', data => {
                setUsername(data['username']);
                setMessages(data['message_objects']);
                setUsersConnected(data['usersConnected'])
                console.log(data)
            })
            Socket.on('new message', data => {
                setMessages([...messages,data['newMessage']])
            })
            Socket.on('addNewUser', data => {
                setUsersConnected([...usersConnected,{'username':data['addNewUser'],'auth_type':data['auth_type']}])
            })
            Socket.on('removeUser', data => {
                let removeUser = data['removeUser']
                setUsersConnected(usersConnected.filter( user => user.username !== removeUser))
            })
            Socket.on('authenticate', data => {
                setUserLoggedIn(data['isAuthenticated']);
            })
            return () => {
                Socket.off('new message');
                Socket.off('addNewUser');
                Socket.off('removeUser');
                Socket.off('authenticate');
            }
        });
    }
    
    getNewAddresses();
    
    return (
            userLoggedIn?
            <div className="container">
                <Header username={username}/>
                <ShowUsers usersConnected={usersConnected} />
                <Messages messages={messages} username={username}/>
                <Form />
            </div>: 
            <Login setUsername={setUsername}/> 
        
    );
}
