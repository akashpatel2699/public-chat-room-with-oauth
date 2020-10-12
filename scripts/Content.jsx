    
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
                setMessages(data['message_objects']);
                setUsersConnected(data['usersConnected'])
                console.log("joinuser")
            })
            Socket.on('new message', data => {
                setMessages([...messages,data['newMessage']])
                console.log(data['newMessage']['created_at'])
            })
            Socket.on('addNewUser', data => {
                setUsersConnected([...usersConnected,data['addNewUser']])
                console.log("addNewUser")
            })
            Socket.on('removeUser', data => {
                let removeUser = data['removeUser']
                setUsersConnected(usersConnected.filter( user => user !== removeUser))
                console.log("removeUser")
            })
            return () => {
                Socket.off('new message');
                Socket.off('addNewUser');
                Socket.off('removeUser');
            }
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