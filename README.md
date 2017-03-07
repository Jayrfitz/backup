# Project2_h2

## Chat room with Facebook and google authorization 

The appilcation is a real-time chat app in the browser, like Google Hangouts, 
Facebook Messenger, or Slack. The User will be able to authenticate who they
are on the chat client by opening the facebook or google and login. 
The chat bot should tell the users that someone new online and there added to 
the user list. But the Bot only resopnse to the commands (!! about). Lastly 
when the user sends a message, the messages in the messages div with the 
user name and profile picture. My bot also has a weather api command  when
(!! weather cityname) is prompted. the messager will also render links and images
through the react message component.
    The points I missed in part 1 that I fixed in part 2 were the !! say, 
!! help, the theme and another command like botname. The theme on the 
chat app is heman chat, the bot will sing heman in text. 
    I tryied to get a audio file to play the heman song on my page it ended up
not working.

Commands are:
!! about
!! help
!! sing
!! joke
!! botname
!! say something
!! weather cityname 


for example (!! weather london)

## Problems


Bot don't write to all the clients when someone logs in or logs out.
users don't get remove from user list when log out occurs.
integration tests

## improvements


I would have like to improvement the userlist and some of the tests.
