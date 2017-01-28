from flask import Flask, request
from sqlalchemy import create_engine
import json
import os

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] =  'mysql://admin:M%m65=N3s-A&ZR3t@mchacks2017.c5se38qdaeio.us-east-1.rds.amazonaws.com:3306/mchacks'

db = create_engine(app.config["SQLALCHEMY_DATABASE_URI"])

@app.before_request
def check_id():
    if request.method == 'POST':
        return "hello"
    
@app.route('/', methods =["POST"] )
def get_con():
    if request.method == "POST":
        json_text = json.dumps({"id": request.args['sessionId']})
        
        return json_text

@app.after_request
def header(response):
    response.headers['Content-type'] = ' application/json'
    return response 
    
    
if __name__ == "__main__":
    app.run(host = "0.0.0.0", port=int(os.environ['PORT']),threaded=True,debug=True)