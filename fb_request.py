from flask import request, render_template, make_response
import os
import json

def json_prettyprint(dictionary):
    print(json.dumps(dictionary,sort_keys=True,indent=4))

# @app.route("/", methods=["POST"])
def receive_message():
    data = json.loads(request.data)
    if (data["object"] == "page"):
        for entry in data["entry"]:
            page_id = entry["id"]
            time_of_event = entry["time"]

            for event in entry["messaging"]:
                if (event["message"]):
                    received_message(event)
                else:
                    print("Webhook received unknown event: " + event)

    return json.dumps({'success':True}), 200, {'ContentType':'application/json'} 

# change subdomain every time!!!!!

# @app.route("/", methods=["GET"])
def fb_auth():
    if (request.args.get('hub.mode') == 'subscribe' and request.args.get('hub.verify_token') == "ni_hao"):
        print("Validating webhook")
        res = make_response(request.args.get('hub.challenge'))
        return res
    else:
        print("Failed validation. Make sure the validation tokens match.")
        resp = make_response(render_template('error.html'), 403)
        return resp
    # print("i'm here")
    # return render_template('test.html')

def received_message(event):
    sender_id = event["sender"]["id"]
    recipient_id = event["recipient"]["id"]
    time_of_message = event["timestamp"]
    message = event["message"]

    print("Received message for user %d and page %d at %d with message:", sender_id, recipient_id, time_of_message)
    print(json.dumps(message))

    message_id = message["mid"]

    message_text = message["text"]
    message_attachments = message["attachments"]

    if (message_text):
        # api.ai call here to parse message_text
    

def send_message(recipient_id, message_text):
    message_data = {
        recipient: {
            id: recipient_id
        },
        message: {
            text: message_text
        }
    }
    call_send_api(json.load(message_data))

def call_send_api(message_data):
    url = "https://graph.facebook.com/v2.6/me/messages"
    payload = {
        page_access_token
    }
    print(os.environ["PAGE_ACCESS_TOKEN"])
    # request.post(url, )
    
# run on port 80

# if __name__ == "__main__":
#     app.run(host='0.0.0.0', port=80)