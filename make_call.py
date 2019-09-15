from twilio.rest import Client
from .auth_info import account_sid, auth_token

def make_call():
    """a code to create a call using twilio API"""

    client = Client(account_sid,auth_token)

    call = client.calls.create(
        url='http://demo.twilio.com/docs/voice.xml',
        to='+17733914873',
        from_='+13126354221'

        )

    return call

if __name__ == "__main__":
    call = make_call()
    print(call.sid)