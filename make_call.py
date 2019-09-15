from twilio.rest import Client
from .auth_info import account_sid, auth_token, account_phone_number, destination_phone_number

def make_call(to_num, from_num):
    """a code to create a call using twilio API"""

    client = Client(account_sid,auth_token)

    call = client.calls.create(
        url='http://demo.twilio.com/docs/voice.xml',
        to=to_num,
        from_=from_num
    )

    return call

if __name__ == "__main__":
    call = make_call(destination_phone_number, account_phone_number)
    print(call.sid)