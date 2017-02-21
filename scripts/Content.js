import * as React from 'react';

import { Button } from './Button';
import { Socket } from './Socket';
// import { UserList } from './UserList';

export class Content extends React.Component {
    constructor(props) {
        super(props);
        this.state = {'messages': []};
        this.state = {'userlist': []};
        
    }
    
    componentDidMount() {
        Socket.on('all messages', (data) => {
            this.setState({
                'messages': data['messages']
            });
        });
        Socket.on('userlist', (data) => {
            this.setState({
                'userlist': data['userlist']
            });
        });
    }
    signOut(event) {
        var auth2 = gapi.auth2.getAuthInstance();
        auth2.signOut();
    }
    
    
    render() {
        let messages = '';
        let userlist =  '';
        if (this.state.messages != null) { 
            messages = this.state.messages.map((n, index) => 
                <li key={index}>
                    <img src={n.picture} />
                    {n.name}: {n.message}
                </li>
             );
        }
        if (this.state.userlist != null) { 
            console.log("############@#@$@$@$");
            userlist = this.state.userlist.map((n, index) => 
                <li key={index}>
                    <img src={n.picture} />
                    {n.name}
                </li>
             );
            console.log(userlist);

        }
        // console.log(messages);
        return (
            <div id="formborder">
                <div>
                     <h1>Message</h1>
                     <div>
                        <h3>chat</h3>
                         <div className="scroll"> 
                            <ul>{messages}</ul>
                         </div>
                         <h3>users</h3>
                         <div className="scroll"> 
                            <ul>{userlist}</ul>
                         </div>
                     </div>
                     
                     <div
                         className="fb-login-button"
                         data-max-rows="1"
                         data-size="large"
                         data-show-faces="true"
                         data-auto-logout-link="true">
                     </div>
                     <div
                        className="g-signin2"
                        data-theme="dark">
                     </div>
                     <div>
                        <a href="#" onClick={this.signOut.bind(this)}>G Sign out</a>
                     </div>
                     <Button />
                     <p>'!! about' for directions</p>
                 </div>
            </div>
        );
    }
}
