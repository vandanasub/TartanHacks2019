# Download the helper library from https://www.twilio.com/docs/python/install
from twilio.rest import Client


# Your Account Sid and Auth Token from twilio.com/console
account_sid = 'ACd79783a9bc6177103987c2b184c2a482'
auth_token = 'c585f20dcb3954f2dbd8b199873a8f37'
client = Client(account_sid, auth_token)

message = client.messages \
                .create(
                     body="Join Earth's mightiest heroes. Like Kevin Bacon.",
                     from_='+12403485434',
                     to='+17034738154'
                 )

print(message.sid)
