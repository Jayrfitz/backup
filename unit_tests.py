import app 
import unittest


class ChatbotResponseTest(unittest.TestCase):
    def test_command(self):
        r = app.chatbot('!! ab')
        self.assertEqual({'picture': 'static/bot.jpg',
        'message': 'not a command', 'link': '', 'name': 'Chat Bot'},r)

    def test_command2(self):
        r = app.chatbot('!! help')
        self.assertEqual(r,{'picture': 'static/bot.jpg', 'message': 
            'HelpYou can login to FacebookYou can login to Gmail'
            'Then you can send messagesbot commands are !! help,'
            '!! sing,!! joke,!! say <something>,!! weather cityname)'
            ' for example!! weather London', 'link': '', 'name': 'Chat Bot'})
    def test_command3(self):
        r = app.chatbot('!! say <something>')
        self.assertEqual(r,{'picture': 'static/bot.jpg',
            'message': '<something>', 'link': '', 'name': 'Chat Bot'})
        
    def test_command4(self):
        r = app.chatbot('!! say       potato')
        self.assertEqual(r,{'picture': 'static/bot.jpg',
            'message': '      potato', 'link': '', 'name': 'Chat Bot'})
        




if __name__ == '__main__':
    unittest.main()