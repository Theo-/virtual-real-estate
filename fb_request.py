from flask import request, render_template, make_response
import requests
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
                if "message" in event:
                    received_message(event)
                else:
                    print(event)

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

def received_message(event):
    sender_id = event["sender"]["id"]
    recipient_id = event["recipient"]["id"]
    time_of_message = event["timestamp"]
    message = event["message"]
    print("Received Message.")

    message_id = message["mid"]

    if "text" in message:
        # api.ai call here to parse message_text
        send_message(sender_id, message["text"])
    else:
        print("echoed back ")
        print(json.dumps(message))

def send_message(recipient_id, message_text):
    message_data = {
        "recipient": json.dumps({
            "id": recipient_id
        }),
        "message": json.dumps({
            "text": message_text
        })
    }
    call_send_api(message_data)

def call_send_api(message_data):
    url = "https://graph.facebook.com/v2.6/me/messages"
    # wow get rid of this shit u idiot
    payload = {
        "access_token": "yourauthhere"
    }
    # print(os.environ.get("PAGE_ACCESS_TOKEN"))
    r = requests.post(url, params=payload, data=message_data)
    print(json.dumps(r.json()))
    
# run on port 80

# if __name__ == "__main__":
#     app.run(host='0.0.0.0', port=80)