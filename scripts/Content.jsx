    
import * as React from 'react';
import  Form  from './Form';
import { Socket } from './Socket';
import Header from './Header';
import Messages from './Messages';
import ShowUsers from './ShowUsers';

export function Content() {
    const [messages, setMessages] = React.useState([]);
    const [username, setUsername] = React.useState("");
    const [usersConnected, setUsersConnected] = React.useState([]);
    
    function getNewAddresses() {
        React.useEffect(() => {
            Socket.on('joinuser', data => {
                setUsername(data['username']);
                setMessages(data['messages']);
                setUsersConnected(data['usersConnected'])
            })
            Socket.on('new messages', data => {
                setMessages([...messages,data['chat']])
            })
            Socket.on('addNewUser', data => {
                setUsersConnected([...usersConnected,data['addNewUser']])
            })
            Socket.on('removeUser', data => {
                 let removeUser = data['removeUser']
                setUsersConnected(usersConnected.filter( user => user !== removeUser))
            })
        });
    }
    
    getNewAddresses();

    return (
        <div>
            <Header username={username}/>
            <ShowUsers usersConnected={usersConnected} />
            <Messages messages={messages} />
            <Form />
        </div>
    );
}
