import * as React from 'react';

import { Socket } from './Socket';

export class Button extends React.Component {
    handleSubmit(event) {
        event.preventDefault();
        
        let message = this.refs.text.value.trim();
        console.log(message);
        FB.getLoginStatus((response) => {
            if (response.status == 'connected') {
                Socket.emit('new message', {
                    'facebook_user_token':
                        response.authResponse.accessToken,
                    'message': message,
                });
            }
        });
        console.log('Sent up the message to server!');
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
