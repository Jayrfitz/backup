import * as React from 'react';

import { Button } from './Button';
import { Socket } from './Socket';
import { Message } from './Message';


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
        Socket.on('remove', (data) => {
            var temp = data['remove'];
            this.setState({
                'name': temp.name
            });
        });
    }

    signOut(event) {
        var auth2 = gapi.auth2.getAuthInstance();
        auth2.signOut();
    }
    
    
    render() {
        let messages = '';
        let userlist = '';
        let userNum  = '';
        console.log(messages);
        if (this.state.messages != null) {
            messages = this.state.messages.map((n, index) => {
                return <Message key={index} src={n.picture} name={n.name} message={n.message} link={n.link} />;
             });
        }
        if (this.state.userlist != null) { 
            
            userlist = this.state.userlist.map((n, index) => 
                <li key={index}>
                    <img src={n.picture} />
                    {n.name}
                </li>
             );
            userNum=this.state.userlist.length;
            console.log(userlist);

        }
        // console.log(messages);
        return (
            <div id="formborder">
                <div>
                     <h1>Heman Chat</h1>
                     <div>
                        <h3>chat</h3>
                         <div className="scroll"> 
                            <ul>{messages}</ul>
                         </div>
                         <div> 
                            <h3>users<ul>{userNum}</ul></h3>
                         </div>
                         
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
                     <p>type '!! about' for directions extra commands '!! sing', '!! joke' more 
                     is specified in about command</p>
                 </div>
            </div>
        );
    }
}
