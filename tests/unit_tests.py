import sys
sys.path.append('..')
import app
import unittest

class ChatbotResponseTest(unittest.TestCase):
    def test_command(self):
        r = app.chatbot('!! ab')
        self.assertEqual('not a command',r)

    def test_command2(self):
        r = app.chatbot('!! help')
        self.assertEqual(r,"""Commands are !! botname, !! about, !! help, !! sing,
!! joke, !! say something,
!! weather cityname for example
!! weather London""")

    def test_command3(self):
        r = app.chatbot('!! say <something>')
        self.assertEqual(r,'<something>')
        
    def test_command4(self):
        r = app.chatbot('!! say       potato')
        self.assertEqual(r,'      potato')
        
    def test_command5(self):
        r = app.chatbot('!! sing')
        self.assertEqual(r,"""And I say hey, yeah, yeah, yeah yay
Hey, yay, yay
I said hey, what's goin' on?""")

    def test_command6(self):
        r = app.chatbot('!! about')
        self.assertEqual(r,"""Whats up dude im chatbot and you are 
chatting us !! help for more""")
    def test_command7(self):
        r = app.chatbot('!! say https://www.facebook.com/jason.fitzgerald.7587')
        self.assertEqual(r,'https://www.facebook.com/jason.fitzgerald.7587')
        
    def test_command8(self):
        r = app.chatbot('sdjkldsjklfsdjklfds !! help')
        self.assertEqual(r,"""Commands are !! botname, !! about, !! help, !! sing,
!! joke, !! say something,
!! weather cityname for example
!! weather London""")
        
        
    def test_command9(self):
        r = app.chatbot('!! say ')
        self.assertEqual(r,'')
        
    def test_command10(self):
        r = app.chatbot('!! botname')
        self.assertEqual(r,'heman bot')
        
    
if __name__ == '__main__':
    unittest.main()