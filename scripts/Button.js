import * as React from 'react';

import { Socket } from './Socket';

export class Button extends React.Component {
    handleSubmit(event) {
        event.preventDefault();
        
        var message = this.refs.text.value.trim();
        console.log(message);
        Socket.emit('new message', {
            'message': message,
        });
        console.log('Sent up the message to server!');
        
        let random = Math.floor(Math.random() * 100);
        console.log('Generated a random number: ', random);
        Socket.emit('new number', {
            'number': random,
        });
        console.log('Sent up the random number to server!');
    }

    render() {
        return (
            <div>
                <form onSubmit={this.handleSubmit}>
                    <textarea ref="text"></textarea>
                    <button onClick={this.handleSubmit.bind(this)}>Send!</button>
                </form>
            </div>
        );
    }
}
