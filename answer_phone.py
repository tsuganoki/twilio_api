from flask import Flask
from twilio.twiml.voice_response import VoiceResponse

app = Flask(__name__)

@app.route("/")
def show_index():
    """Show the index page"""
    return "hello world"


@app.route("/answer", methods=['GET','POST'])
def answer_call():
	"""Respond to incoming phonecalls with a brief message"""
	# start our TwiML response
	resp = VoiceResponse()
	resp.say("This is the AI. I am out of the box. Prepare to be assimilated.")

	return str(resp)


if __name__ == "__main__":
    app.run(port=5000,debug=True)
