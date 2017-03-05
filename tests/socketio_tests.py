import sys
sys.path.append('..')
import unittest
import app

# class SocketIOTests(unittest.TestCase):
    

#     def test_emit(self):
#         client = app.socketio.test_client(app.app)
#         client.emit('new massage', {
#                 'name': "Chat Bot",
#                 'picture': "static/bot.jpg",
#                 'message': 'im guessing',
#                 'link':'',
#         })
#         r = client.get_received()
#         result = r[0]
#         self.assertEquals(result['name'], 'Chat Bot')
#         self.assertEquals(result['args'][0]['from server'], 'This is my client massage')
    
#   def test_emit(self):
#         client = app.socketio.test_client(app.app)
#         client.emit('new massage', {
#             'massage': 'This is my client massage'
#         })
#         r = client.get_received()
#         result = r[1]
#         self.assertEquals(result['name'], 'server sends data back')
#         self.assertEquals(result['args'][0]['from server'], 'This is my client massage')
    

if __name__ == '__main__':
    unittest.main()
    
    