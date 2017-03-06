import sys
sys.path.append('..')
import app
import flask 
from flask import Flask
from flask_socketio import SocketIO, send
import unittest

app = Flask(__name__)
socketio = SocketIO(app)

@socketio.on('connect')
def on_connect():
    send('connected')
    
@socketio.on('disconnect')
def on_disconnect():
    global disconnected
    disconnected = '/'


class ChatbotResponseTest(unittest.TestCase):

    def test_connect(self):
        client = socketio.test_client(app)
        received = client.get_received()
        self.assertEqual(len(received), 1)
        self.assertEqual(received[0]['args'], 'connected')
        client.disconnect()
    def test_disconnect(self):
        global disconnected
        disconnected = None
        client = socketio.test_client(app)
        client.disconnect()
        self.assertEqual(disconnected, '/')
    
    
    
    
    
    
    
if __name__ == '__main__':
    unittest.main()