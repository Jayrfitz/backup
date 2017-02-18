import * as React from 'react';

import { Button } from './Button';
import { Socket } from './Socket';

export class Content extends React.Component {
    constructor(props) {
        super(props);
        // this.state = {'numbers': []};
        this.state = {'messages': []};
        
    }
    
    

    componentDidMount() {
        Socket.on('all messages', (data) => {
            this.setState({
                'messages': data['messages']
            });
        });
        // Socket.on('all numbers', (data) => {
        //     this.setState({
        //         'numbers': data['numbers']
        //     });
        // });
    }
    
    render() {
        // let numbers = this.state.numbers.map(
        //     (n, index) => <li className="number-item" key={index}>{n}</li>
        // );
        let messages = this.state.messages.map(
            (n, index) => <li className="message-item" key={index}>{n}</li>
        );
        console.log(messages);
        return (
            <div>
                 
                 <h1>Random number and message!</h1>
                 <ul>{messages}</ul>
                 <div
                     className="fb-login-button"
                     data-max-rows="1"
                     data-size="medium"
                     data-show-faces="false"
                     data-auto-logout-link="true">
                 </div>
                 <Button />
                 
            
            </div>
        );
    }
}
