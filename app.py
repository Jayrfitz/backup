import os
import flask 
import flask_socketio
import requests
import flask_sqlalchemy
import json
from flask import Flask, request

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
    global user
    user = request.sid
    print user
    print 'Someone connected!'

@socketio.on('disconnect')
def on_disconnect():
    global user
    print 'Someone disconnected!'
    
all_mah_message = []
all_mah_user = []


def getmessages():
    messageQuery = models.Message.query.all()
    all_mah_message = []
    for i in range (0, len(messageQuery)):
        message = { 'message':messageQuery[i].message,'name':messageQuery[i].name,'picture':messageQuery[i].picture}
        all_mah_message.append(message)
    return all_mah_message

def commitMessage(message):
    all_mah_message.append(message)
    message = models.Message(message['name'],message['picture'],message['message'])
    models.db.session.add(message)  
    models.db.session.commit()
    
def botApi(apiCity):
    print apiCity
    # response = requests.get('api.openweathermap.org/data/2.5/weather?q='+ apiCity+ '&appid=' + os.environ['KEY'])
    response = requests.get('http://api.openweathermap.org/data/2.5/weather?q='+ apiCity+ '&appid=5fea858a2b422296f20a8654c22fdd72')
    json_body = response.json()
    
    # print "******jsonWeather******** =", json_body['weather'][0]['description']
    city = json_body['name']
    weather = json_body['weather'][0]['description']
    api = city + ' weather description: '+ weather
    # json_body["images"][random_int]["display_sizes"][0]["uri"]
    return api
        
# # ###########################################################################
# # chat bot    
def chatbot(data, all_mah_message):
    botmessage = ''
    if "!! " in data['message']:
        if "!! about" in data['message']:
            print "Bot says what"
            botmessage = {
                'name': "Chat Bot",
                'picture': "static/bot.jpg",
                'message': "Whats up dude im chatbot and you are chatting, whats up with that?"
                "Commands are !! help,!! sing,!! joke,!! say <something>",
            }
        elif "!! help" in data['message']:
            print "Bot says what"
            botmessage = {
                'name': "Chat Bot",
                'picture': "static/bot.jpg",
                'message': "Help\n"
                "You can login to Facebook\n"
                "You can login to Gmail\n"
                "Then you can send messages\n"
                "I wish i could tell you more\n",
            }
            
        elif "!! sing" in data['message']:
            print "Bot says what"
            botmessage = {
                'name': "Chat Bot",
                'picture': "static/bot.jpg",
                'message': "I am not your robot, I am not a clone. "
                "You are not my puppeteer and I am not a drone. "
                "Got a new master and I follow Him alone. "
                "I want a good life till I'm gone. ",
            }
          
        elif "!! joke" in data['message']:
            print "Bot says what"
            botmessage = {
                'name': "Chat Bot",
                'picture': "static/bot.jpg",
                'message': "If the robot does the robot, is it just dancing?",
            }
            
        elif "!! say " in data['message']:
            print "Bot says what"
            data['message'] = data['message'].replace("!! say ", "")
            botmessage = {
                'name': "Chat Bot",
                'picture': "static/bot.jpg",
                'message': data['message'],
            }
        elif "!! weather " in data['message']:
            print "Bot says what"
            data['message'] = data['message'].replace("!! weather ", "")
            apiCity = data['message']
            weather = botApi(apiCity)
            botmessage = {
                'name': "Chat Bot",
                'picture': "static/bot.jpg",
                'message': weather,
            }
        else:
            print "Bot says what"
            botmessage = {
                'name': "Chat Bot",
                'picture': "static/bot.jpg",
                'message': "not a command",
            }
        commitMessage(botmessage)
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
        message = {
            'name': json['name'],
            'picture': json['picture']['data']['url'],
            'message': data['message'],
        }
        
        # print "Got an event for new message with data:", data
        
        all_mah_message = getmessages()
        all_mah_message.append(message)
        commitMessage(message)
        botmessage = chatbot(data,all_mah_message)
        if botmessage != "":
            all_mah_message.append(botmessage)
        
        
        
        
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
        
        message = {
            'name': json['name'],
            'picture': json['picture'],
            'message': data['message'],
        }
        # print "Got an event for new message with data:", data
        
        all_mah_message = getmessages()
        all_mah_message.append(message)
        commitMessage(message)
        botmessage = chatbot(data,all_mah_message)
        if botmessage != "":
            all_mah_message.append(botmessage)
        
        
        
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
    # print all_mah_message
    # print all_mah_user
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
