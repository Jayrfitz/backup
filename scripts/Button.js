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
                    'google_user_token': '',
                    'facebook_user_token':
                        response.authResponse.accessToken,
                    'message': message,
                });
            } else {
                let auth = gapi.auth2.getAuthInstance();
                let user = auth.currentUser.get();
                if (user.isSignedIn()) {
                    Socket.emit('new message', {
                        'google_user_token':
                            user.getAuthResponse().id_token,
                        'facebook_user_token': '',
                        'message': message,
                    });
                }
            }
            
        });
        console.log('Sent up the message to server!');
    }

    render() {
        return (
            <div>
                <form onSubmit={this.handleSubmit}>
                    <textarea ref="text" rows="2" cols="50"></textarea>
                    <button onClick={this.handleSubmit.bind(this)}>Send!</button>
                </form>
            </div>
        );
    }
}
