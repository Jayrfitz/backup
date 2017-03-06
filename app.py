import os
import flask 
import flask_socketio
import requests
import flask_sqlalchemy
import json
from flask import Flask, request
from flask_socketio import SocketIO, send

app = flask.Flask(__name__)
socketio = flask_socketio.SocketIO(app)

import models

@app.route('/')
def hello():
    return flask.render_template('index.html')
    
user = ''
disconnect = ''
@socketio.on('connect')
def on_connect():
    send('connected')

@socketio.on('disconnect')
def on_disconnect():
    global disconnected
    disconnected = '/'
    
all_mah_message = []
all_mah_user = []

# # ###########################################################################
# # get messages database
def getmessages():
    messageQuery = models.Message.query.all()
    all_mah_message = []
    for i in range (0, len(messageQuery)):
        message = { 'message':messageQuery[i].message,'name':messageQuery[i].name,'picture':messageQuery[i].picture}
        all_mah_message.append(message)
    return all_mah_message
# # ###########################################################################
# # commit messages to database
def commitMessage(message):
    all_mah_message.append(message)
    message = models.Message(message['name'],message['picture'],message['message'],message['link'])
    models.db.session.add(message)  
    models.db.session.commit()
    

# # ###########################################################################
# # bot api    
def botApi(apiCity):
    print apiCity
    response = requests.get('http://api.openweathermap.org/data/2.5/weather?q='+ apiCity+ '&appid=' + os.environ['KEY'])
    json_body = response.json()
    
    
    city = json_body['name']
    weather = json_body['weather'][0]['description']
    api = city + ' weather description: '+ weather
    return api
        
# # ###########################################################################
# # chat bot    
def chatbot(message):
    botmessage = ''
    if "!! " in message:
        if "!! about" in message:
            print "Bot says what"
            botmessage = """Whats up dude im chatbot and you are 
chatting use !! help for more"""
                
        elif "!! help" in message:
            print "Bot says what"
            botmessage = """Commands are !! botname, !! about, !! help, !! sing,
!! joke, !! say something,
!! weather cityname for example
!! weather London"""
            
        elif "!! sing" in message:
            print "Bot says what"
            botmessage = """And I say hey, yeah, yeah, yeah yay
Hey, yay, yay
I said hey, what's goin' on?"""
          
        elif "!! joke" in message:
            print "Bot says what"
            botmessage ="If the robot does the robot, is it just dancing?"
        
        elif "!! botname" in message:
            print "Bot says what"
            botmessage ="heman bot"
            
            
        elif "!! say " in message:
            print "Bot says what"
            message = message.replace("!! say ", "")
            botmessage = message
            
        elif "!! weather " in message:
            print "Bot says what"
            message = message.replace("!! weather ", "")
            apiCity = message
            weather = botApi(apiCity)
            botmessage = weather
        else:
            print "Bot says what"
            botmessage = "not a command"
        return(botmessage)
    else:
        return(botmessage)
    
    
@socketio.on('new message')
def on_new_message(data):
############################################################################
# facebook request 
    
    global user
    if data['google_user_token']== '':
        isTrue = False 
        response = requests.get('https://graph.facebook.com/v2.8/me?fields=id%2Cname%2Cpicture&access_token='
        + data['facebook_user_token'])
        json = response.json()
        
        
        #########################################
        #link and jpg,png
        mess = data['message']
        
        end = mess[-4:]
        end5 = mess[-5:]
        link = ''
        if end == '.png' or end == '.jpg' or end == '.gif':
            link = 'img'
        elif end5 == '.jpeg':
            link = 'img'
        else:
            link = ''

        print link
        
        
        
        message = {
            'name': json['name'],
            'picture': json['picture']['data']['url'],
            'message': data['message'],
            'link': link,
            
        }
        
   
        
        all_mah_message = getmessages()
        all_mah_message.append(message)
        commitMessage(message)
        botmessage = chatbot(data['message'])
        
        if botmessage != "":
            message = {
                'name': "Chat Bot",
                'picture': "static/bot.jpg",
                'message': botmessage,
                'link':'',
            }
            commitMessage(message)
            all_mah_message.append(message)
            
        ####### userlist
        
        for k in all_mah_user:
           if json['name'] == k['name']:
               isTrue = True
              
             
        if not isTrue:        
            all_mah_user.append({
            'name': json['name'],
            'picture': json['picture']['data']['url'],
            'user': user,
            })
        
        
############################################################################
# google request   
    elif data['facebook_user_token']== '':
        isTrue = False 
        response = requests.get('https://www.googleapis.com/oauth2/v3/tokeninfo?id_token='
        + data['google_user_token'])
        json = response.json()
        
        
        #########################################
        #link and jpg,png
        mess = data['message']

        end = mess[-4:]
        end5 = mess[-5:]
        link = ''
        if end == '.png' or end == '.jpg' or end == '.gif':
            link = 'img'
        elif end5 == '.jpeg':
            link = 'img'
        else:
            link = ''

        print link
        
        message = {
            'name': json['name'],
            'picture': json['picture'],
            'message': data['message'],
            'link': link,
            
        }
        
        all_mah_message = getmessages()
        all_mah_message.append(message)
        commitMessage(message)
        botmessage = chatbot(data['message'])
        
        if botmessage != "":
            message = {
                'name': "Chat Bot",
                'picture': "static/bot.jpg",
                'message': botmessage,
                'link':'',
            }
            commitMessage(message)
            all_mah_message.append(message)
        
        
        ##### userlist
        for k in all_mah_user:
           if json['name'] == k['name']:
               isTrue = True
              
             
        if not isTrue:        
            all_mah_user.append({
            'name': json['name'],
            'picture': json['picture'],
            'user': user,
            })
        
    socketio.emit('all messages', {
        'messages': all_mah_message
    })
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
