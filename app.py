from flask import Flask, request, jsonify, Response
from twilio.twiml.messaging_response import MessagingResponse
from twilio.rest import Client 
import os

account_sid = os.environ['account_sid_']
auth_token = os.environ['auth_token_']
client = Client(account_sid, auth_token) 

app = Flask(__name__)

@app.route('/')
def main():
    return "HELLO"

@app.route('/sms', methods=['POST', 'GET'])
def sms_reply():
    msg_type = request.form.get('msg_type', 'phone')
    print(msg_type)
    
    # fetching incoming message
    #msg = request.form.get('Body')

    #Create reply
    #resp = MessagingResponse()
    #resp.message("hola tu dijiste {}".format(msg))

    #return str(resp)
    #print(request.form.get('Body'))
    msg_from_post = request.form.get('msg')

    if msg_type == "phone":
        to_phone_number = request.form.get('to_phone_number')
        print(msg_from_post, to_phone_number)
        message = client.messages.create(to=f'whatsapp:+{to_phone_number}', from_='whatsapp:+14155238886', body=msg_from_post ) 
        print(message.sid)
        status_code = Response(status=201)
        return status_code

    elif msg_type=="broadcast":
        to = []
        for msgs in client.messages.list():
            if("Join" in msgs.body):
                if msgs.from_.replace('whatsapp:+','') not in to:
                    to.append(msgs.from_.replace('whatsapp:+',''))
                
        print("#########################################################################")
        print(to)
        for number in to:
            client.messages.create(to=f'whatsapp:+{number}', from_='whatsapp:+14155238886', body=msg_from_post )
        status_code = Response(status=201)
        return status_code
    
@app.route('/users')
def get_users():
    to = []
    for msgs in client.messages.list():
        if("Join" in msgs.body):
            if msgs.from_.replace('whatsapp:+','') not in to:
                to.append(msgs.from_.replace('whatsapp:+',''))
    
    for number in to:
        print(number)
    return jsonify(to)

if __name__ == '__main__':
    app.run(debug=True)