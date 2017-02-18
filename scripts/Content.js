import * as React from 'react';

import { Button } from './Button';
import { Socket } from './Socket';

export class Content extends React.Component {
    constructor(props) {
        super(props);
        this.state = {
            'numbers': []
        };
    }

    componentDidMount() {
        Socket.on('all numbers', (data) => {
            this.setState({
                'numbers': data['numbers']
            });
        });
    }

    render() {
        let numbers = this.state.numbers.map(
            (n, index) => <li className="number-item" key={index}>{n}</li>
        );
        return (
            <div>
             <h1>Random numbers by person!</h1>
             <div
                 className="fb-login-button"
                 data-max-rows="1"
                 data-size="medium"
                 data-show-faces="false"
                 data-auto-logout-link="true">
             </div>
             <Button />
             <ul>{numbers}</ul>
            </div>
        );
    }
}
