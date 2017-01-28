from flask import Flask, request
 
import json
import os

app = Flask(__name__)

@app.route('/', methods =["POST"] )
def get_con():
    if request.method == "POST":
        return json.dumps({"param" :request.args['sessionId']})
    

if __name__ == "__main__":
    app.run(port=os.environ['PORT'],threaded=True,debug=True)