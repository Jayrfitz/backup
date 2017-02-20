import os
import flask
import flask_socketio
import requests
import flask_sqlalchemy

app = flask.Flask(__name__)
socketio = flask_socketio.SocketIO(app)

import models
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://potato:potatosareawesome@localhost/postgres'
db = flask_sqlalchemy.SQLAlchemy(app)

@app.route('/')
def hello():
    return flask.render_template('index.html')
    

@socketio.on('connect')
def on_connect():
    print 'Someone connected!'

@socketio.on('disconnect')
def on_disconnect():
    print 'Someone disconnected!'
    
all_mah_message = []

@socketio.on('new message')
def on_new_message(data):
    
    response = requests.get('https://graph.facebook.com/v2.8/me?fields=id%2Cname%2Cpicture&access_token='
    + data['facebook_user_token'])
    json = response.json()

    
    print "Got an event for new message with data:", data

    all_mah_message.append({
        'name': json['name'],
        'picture': json['picture']['data']['url'],
        'message': data['message'],
    })
    
    message = models.Message(all_mah_message)
    models.db.session.add(message)
    all_mah_message.append(models.Message.query.all())
    
    socketio.emit('all messages', {
        'messages': all_mah_message
    })
if __name__ == '__main__':
    socketio.run(
        app,
        host=os.getenv('IP', '0.0.0.0'),
        port=int(os.getenv('PORT', 8080)),
        debug=True
    )
