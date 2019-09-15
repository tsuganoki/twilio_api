from twilio.rest import Client


def make_call():
    """a code to create a call using twilio API"""
    account_sid = open("account_sid.txt","r+")

    auth_token = open("auth_token.txt","r+")

    client = Client(account_sid.read(),auth_token.read())

    call = client.calls.create(
        url='http://demo.twilio.com/docs/voice.xml',
        to='+17733914873',
        from_='+13126354221'

        )

    return call.sid

if __name__ == "__main__":
    make_call()