from twilio.rest import Client
import openai
from flask import Flask, jsonify, request
import os

def getTwilioClient():
    twilio_account_sid = os.getenv('TWILIO_ACCOUNT_SSID')
    twilio_account_secret = os.getenv('TWILIO_ACCOUNT_SECRET')
    client = Client(twilio_account_sid, twilio_account_secret)
    return client

def getOpenAiClient():
    openai.api_key = os.getenv('OPENAI_API_KEY')
    return openai


def getChatGPTResponse(input):
    response = getOpenAiClient().ChatCompletion.create(
        model="gpt-3.5-turbo", 
        messages=[
            {"role": "user", "content": input}
        ]
    )
    return response["choices"][0]["message"]["content"]

def sendWhatsappMessage(message):
    twilio_hosted_whatsapp_number = 'whatsapp:' + os.getenv('TWILIO_HOSTED_WHATSAPP_NUMBER')
    personal_whatsapp_number = 'whatsapp:' + os.getenv('PERSONAL_WHATSAPP_NUMBER')

    message = getTwilioClient().messages \
                .create(
                     body= message ,
                     from_= twilio_hosted_whatsapp_number,
                     to= personal_whatsapp_number
                 )

app = Flask(__name__)

@app.route('/', methods=['GET'])
def receiveDefault():
    response = jsonify(success=True)
    return response

@app.route('/routineWhatsapp', methods=['POST'])
def receive():
    record = request.values.get('Body', None)
    chatGPTResponse = getChatGPTResponse(record)
    sendWhatsappMessage(chatGPTResponse)
    response = jsonify(success=True)
    return response

if __name__ == '__main__':
    app.run()