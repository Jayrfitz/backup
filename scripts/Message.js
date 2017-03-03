import * as React from 'react';

export class Message extends React.Component {
    
    


    render() {
        // console.log(this.props.link);
        let message;
        var protoPattern = new RegExp("((ftp|http|https):\/\/)?[a-zA-Z0-9\-\.]+\.[a-zA-Z]{2,3}(\/\S*)?");
        var urlPattern = new RegExp("\.(com|edu|gov|org)");
        var propRes = protoPattern.test(this.props.message);
        var urlRes = urlPattern.test(this.props.message);
        if(this.props.link === 'img'){
            console.log("this is an image in userMessage");
            message = <img className="images" src={this.props.message}/>;  
        }
        else if(propRes && urlRes){
            console.log("this link *****");
            message = <a href={this.props.message} target="_blank">{this.props.message}</a>;
        }
        else {
            message = this.props.message;
        }

        return (
        <div>
       <li key={this.props.key}>
        <img src={this.props.src} />
             {this.props.name}: {message}</li>
        
        </div>
        );

    }
}