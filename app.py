from flask import Flask
from sqlalchemy import create_engine

app = Flask(__name__)

@app.route('/')
def hello_world():
    return 'Hello, World!'

app.config['SQLALCHEMY_DATABASE_URI'] = \
    'mysql://admin:M%m65=N3s-A&ZR3t@mchacks2017.c5se38qdaeio.us-east-1.rds.amazonaws.com:3306/mchacks'

db = create_engine(app.config["SQLALCHEMY_DATABASE_URI"])

@app.route('/getCon', methods =["POST"] )
def get_con():
    pass



if __name__ == "__main__":
    app.run(port=5000,threaded=True,debug=True)