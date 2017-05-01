import os
import sys
import json

import requests
from flask import Flask, request


app = Flask(__name__)

flag = 0


@app.route('/', methods=['GET'])
def verify():
    # when the endpoint is registered as a webhook, it must echo back
    # the 'hub.challenge' value it receives in the query arguments
    if request.args.get("hub.mode") == "subscribe" and request.args.get("hub.challenge"):
        if not request.args.get("hub.verify_token") == os.environ["VERIFY_TOKEN"]:
            return "Verification token mismatch", 403
        return request.args["hub.challenge"], 200

    return "Hello world", 200


@app.route('/', methods=['POST'])
def webhook():

    # endpoint for processing incoming messaging events

    data = request.get_json()
    log(data)  # you may not want to log every incoming message in production, but it's good for testing

    if data["object"] == "page":

        for entry in data["entry"]:
            
            for messaging_event in entry["messaging"]:

                if messaging_event.get("message"):  # someone sent us a message

                    sender_id = messaging_event["sender"]["id"]        # the facebook ID of the person sending you the message
                    recipient_id = messaging_event["recipient"]["id"]  # the recipient's ID, which should be your page's facebook ID
                    message_text = messaging_event["message"]["text"]  # the message's text
                    
                    words = message_text.split(",")
                    log(words)
                    if len(words)>=3:
                        outbounddate = words[0]
                        origin = words[1]
                        destination = words[2]
                    else:
                        outbounddate = "2017-07-07"
                        origin = "IST"
                        destination = "ESB"

                    url ="http://partners.api.skyscanner.net/apiservices/browseroutes/v1.0/TR/usd/tr-TR/%s/%s/%s/?apikey=prtl6749387986743898559646983194" % (origin, destination, outbounddate)
                    
                    #url ="http://partners.api.skyscanner.net/apiservices/browseroutes/v1.0/TR/usd/tr-TR/IST/ESB/2017-10-25/2017-11-11?apikey=prtl6749387986743898559646983194"
                    log(url)
                    f = requests.get(url)
                    json_data = json.loads(f.text)

#str1 = "Available flights from " + origin + " to " + destination + " with prices: "
                    str1 = "Available flights with prices: "
                    if flag==0:
                        for item in json_data["Quotes"]:
                            str1 = str1 + str(item["MinPrice"]) + ", "

                    log(str1)

                    send_message(sender_id, str1)
                

                if messaging_event.get("delivery"):  # delivery confirmation
                    pass

                if messaging_event.get("optin"):  # optin confirmation
                    pass

                if messaging_event.get("postback"):  # user clicked/tapped "postback" button in earlier message
                    pass

    return "ok", 200


def send_message(recipient_id, message_text):
    

    log("sending message to {recipient}: {text}".format(recipient=recipient_id, text=message_text))

    params = {
        "access_token": os.environ["PAGE_ACCESS_TOKEN"]
    }
    headers = {
        "Content-Type": "application/json"
    }
    data = json.dumps({
        "recipient": {
            "id": recipient_id
        },
        "message": {
            "text": message_text
        }
    })
    flag=1
    r = requests.post("https://graph.facebook.com/v2.6/me/messages", params=params, headers=headers, data=data)
    if r.status_code != 200:
        log(r.status_code)
        log(r.text)


def log(message):  # simple wrapper for logging to stdout on heroku
    print str(message)
    sys.stdout.flush()


if __name__ == '__main__':
    app.run(debug=True)
