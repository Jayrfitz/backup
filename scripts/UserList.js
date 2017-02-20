// import * as React from 'react';

// import { Socket } from './Socket';


// export class UsersList extends React.Component {
//     constructor(props) {
//         super(props);
//         this.state = {'messages': []};
        
//     }
    
//     componentDidMount() {
//         Socket.on('add user', (data) => {
//             this.setState({
//                 'messages': data['messages']
//             });
//         });
//     }
//     render() {
//         let messages = this.state.messages.map((n, index) => 
//             <li key={index}>
//                 <img src={n.picture} />
//                 {n.name}
//             </li>
//          );
//         return (
//           <div className='users'>
//               <h3> Online Users </h3>
//               <ul>
//                   {messages}
//               </ul>                
//           </div>
//         );
//     }
// }
