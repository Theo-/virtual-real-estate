from flask import Flask, request
 
import json
import os

app = Flask(__name__)

@app.route('/', methods =["POST"] )
def get_con():
    if request.method == "POST":
        return json.dumps({{
"speech": "Barack Hussein Obama II is the 44th and current President of the United States.",
"displayText": "Barack Hussein Obama II is the 44th and current President of the United States, and the first African American to hold the office. Born in Honolulu, Hawaii, Obama is a graduate of Columbia University   and Harvard Law School, where ",
}})
    

if __name__ == "__main__":
    app.run(host = "0.0.0.0", port=int(os.environ['PORT']),threaded=True,debug=True)