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
    # socketio.emit('add user', {
    #     'messages': all_mah_message
    # })
    # all_mah_message.append({
    #         'name': "Chat Bot",
    #         'picture': "static/bot.jpg",
    #         'message': "Hello this is a chatroom don't end up on To Catch a predator",
    #     })
    print 'Someone connected!'

@socketio.on('disconnect')
def on_disconnect():
    # all_mah_message.append({
    #         'name': "Chat Bot",
    #         'picture': "static/bot.jpg",
    #         'message': "Bye",
    #     })
    print 'Someone disconnected!'
    
all_mah_message = []

@socketio.on('new message')
def on_new_message(data):
# ###########################################################################
# facebook request   
    if data['google_user_token']== '':
        response = requests.get('https://graph.facebook.com/v2.8/me?fields=id%2Cname%2Cpicture&access_token='
        + data['facebook_user_token'])
        json = response.json()
        
        
        print "Got an event for new message with data:", data
        # all_mah_message.append(data['message'])
        all_mah_message.append({
            'name': json['name'],
            'picture': json['picture']['data']['url'],
            'message': data['message'],
        })
# ###########################################################################
# google request   
    elif data['facebook_user_token']== '':
        response = requests.get('https://www.googleapis.com/oauth2/v3/tokeninfo?id_token='
        + data['google_user_token'])
        json = response.json()
        
        
        print "Got an event for new message with data:", data
        # all_mah_message.append(data['message'])
        all_mah_message.append({
            'name': json['name'],
            'picture': json['picture'],
            'message': data['message'],
        })
        
# ###########################################################################
# chat bot
        
    if "!! about" in data['message']:
        print "Bot says what"
        all_mah_message.append({
            'name': "Chat Bot",
            'picture': "static/bot.jpg",
            'message': "Whats up dude im chatbot and you are chatting, whats up with that?",
        })
    if "!! help" in data['message']:
        print "Bot says what"
        all_mah_message.append({
            'name': "Chat Bot",
            'picture': "static/bot.jpg",
            'message': "Help\n"
            "You can login to Facebook\n"
            "You can login to Gmail\n"
            "Then you can send messages\n"
            "I wish i could tell you more\n",
        })
      
      
      
    
    # #message = models.Message(all_mah_message)
    # #models.db.session.add(message)
    # #all_mah_message.append(models.Message.query.all())
    
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
