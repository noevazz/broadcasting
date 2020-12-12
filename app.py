from flask import Flask, request
from twilio.twiml.messaging_response import MessagingResponse
from twilio.rest import Client 
import os


app = Flask(__name__)

@app.route('/')
def main():
    return "HELLO"

@app.route('/sms', methods=['POST', 'GET'])
def sms_reply():
    account_sid = os.environ['account_sid_']
    auth_token = os.environ['auth_token_']
    client = Client(account_sid, auth_token) 
    # fetching incoming message
    #msg = request.form.get('Body')

    #Create reply
    #resp = MessagingResponse()
    #resp.message("hola tu dijiste {}".format(msg))

    #return str(resp)
    print(request.form.get('Body'))

    msg_from_post = request.form.get('msg')
    to_phone_number = request.form.get('to_phone_number')
    print(msg_from_post, to_phone_number)
    message = client.messages.create(to=f'whatsapp:+{to_phone_number}', from_='whatsapp:+14155238886', body=msg_from_post ) 
 
    print(message.sid)
    return message.sid

if __name__ == '__main__':
    app.run(debug=True)