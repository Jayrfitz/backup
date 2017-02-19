import os
import flask
import flask_socketio
import requests

app = flask.Flask(__name__)
socketio = flask_socketio.SocketIO(app)

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
    print "*json1*", json, "*json2*"
    
    # all_mah_message.append(data['message'])
    all_mah_message.append({
        'name': json['name'],
        'picture': json['picture']['data']['url'],
        'message': data['message'],
    })
    
    socketio.emit('all messages', {
        'messages': all_mah_message
    })

socketio.run(
    app,
    host=os.getenv('IP', '0.0.0.0'),
    port=int(os.getenv('PORT', 8080)),
    debug=True
)


    
