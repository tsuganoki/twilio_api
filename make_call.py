from twilio.rest import Client

account_sid = open("account_sid.txt","r+")

auth_token = open("auth_token.txt","r+")

client = Client(account_sid.read(),auth_token.read())

call = client.calls.create(
    url='http://demo.twilio.com/docs/voice.xml',
    to='+17733914873',
    from_='+13126354221'

    )

print(call.sid)