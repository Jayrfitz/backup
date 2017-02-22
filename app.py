import os
import flask 
import flask_socketio
import requests
import flask_sqlalchemy
from flask import Flask, request
app = flask.Flask(__name__)
socketio = flask_socketio.SocketIO(app)

import models
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://potato:potatosareawesome@localhost/postgres'
db = flask_sqlalchemy.SQLAlchemy(app)

@app.route('/')
def hello():
    return flask.render_template('index.html')
    
user = ''
disconnect = ''
@socketio.on('connect')
def on_connect():
    global user
    user = request.sid
    print user
    print 'Someone connected!'

@socketio.on('disconnect')
def on_disconnect():
    global user
    temp = ""
    for k in user:
        print k
        if(request.sid == k['user_id']):
            temp = user.pop(user.index(k))
            user.remove(k)
    print temp
    socketio.emit('userlist', {
        'userlist': user
        })
    socketio.emit('remove', {
        'remove': temp
        })
    print 'Someone disconnected!'
    
all_mah_message = []
all_mah_user = []

@socketio.on('new message')
def on_new_message(data):
# ###########################################################################
# facebook request 
    global user
    if data['google_user_token']== '':
        isTrue = False 
        response = requests.get('https://graph.facebook.com/v2.8/me?fields=id%2Cname%2Cpicture&access_token='
        + data['facebook_user_token'])
        json = response.json()
        
        
        # print "Got an event for new message with data:", data
        # all_mah_message.append(data['message'])
        all_mah_message.append({
            'name': json['name'],
            'picture': json['picture']['data']['url'],
            'message': data['message'],
        })
        for k in all_mah_user:
           if(json['name'] == k['name']):
               isTrue = True
              
             
        if not isTrue:        
            all_mah_user.append({
            'name': json['name'],
            'picture': json['picture']['data']['url'],
            'user': user,
            })
        
        
# ###########################################################################
# google request   
    elif data['facebook_user_token']== '':
        isTrue = False 
        response = requests.get('https://www.googleapis.com/oauth2/v3/tokeninfo?id_token='
        + data['google_user_token'])
        json = response.json()
        
        
        # print "Got an event for new message with data:", data
        # all_mah_message.append(data['message'])
        for k in all_mah_user:
           if(json['name'] == k['name']):
               isTrue = True
              
             
        if not isTrue:        
            all_mah_user.append({
            'name': json['name'],
            'picture': json['picture'],
            'user': user,
            })
        all_mah_message.append({
            
            'name': json['name'],
            'picture': json['picture'],
            'message': data['message'],
        })
        
        
        
# ###########################################################################
# chat bot
    if "!! " in data['message']:
        if "!! about" in data['message']:
            print "Bot says what"
            all_mah_message.append({
                'name': "Chat Bot",
                'picture': "static/bot.jpg",
                'message': "Whats up dude im chatbot and you are chatting, whats up with that?"
                "Commands are !! help,!! sing,!! joke,!! say <something>",
            })
        elif "!! help" in data['message']:
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
            
        elif "!! sing" in data['message']:
            print "Bot says what"
            all_mah_message.append({
                'name': "Chat Bot",
                'picture': "static/bot.jpg",
                'message': "I am not your robot, I am not a clone. "
                "You are not my puppeteer and I am not a drone. "
                "Got a new master and I follow Him alone. "
                "I want a good life till I'm gone. ",
            })
          
        elif "!! joke" in data['message']:
                print "Bot says what"
                all_mah_message.append({
                'name': "Chat Bot",
                'picture': "static/bot.jpg",
                'message': "If the robot does the robot, is it just dancing?",
            })
            
        elif "!! say <" in data['message']:
            print "Bot says what"
            data['message'] = data['message'].replace("!! say <", "")
            data['message'] = data['message'].replace(">", "")
            all_mah_message.append({
            'name': "Chat Bot",
            'picture': "static/bot.jpg",
            'message': data['message'],
            })
        else:
            print "Bot says what"
            all_mah_message.append({
            'name': "Chat Bot",
            'picture': "static/bot.jpg",
            'message': "not a command",
            })
      
      
    
    # #message = models.Message(all_mah_message)
    # #models.db.session.add(message)
    # #all_mah_message.append(models.Message.query.all())
    
    socketio.emit('all messages', {
        'messages': all_mah_message
    })
    print all_mah_message
    print all_mah_user
    socketio.emit('userlist', {
        'userlist': all_mah_user
        })
if __name__ == '__main__':
    socketio.run(
        app,
        host=os.getenv('IP', '0.0.0.0'),
        port=int(os.getenv('PORT', 8080)),
        debug=True
    )