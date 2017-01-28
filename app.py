from flask import Flask, request
 
import json

app = Flask(__name__)

@app.route('/', methods =["POST"] )
def get_con():
    if request.method == "POST":
        return json.dumps({"param" :request.args['sessionId']})
    

if __name__ == "__main__":
    app.run(port=80,threaded=True,debug=True)