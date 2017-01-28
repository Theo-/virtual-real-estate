from flask_sqlalchemy import SQLAlchemy
from flask import Flask, request, render_template
from flask_migrate import Migrate, MigrateCommand
from flask_script import Manager, Server
from models import User, Classifiers, Listing, ListingImage, ListingMappedImages, UserVisitedListings, Base
import json
import os

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] =  'mysql+pymysql://admin:M%m65=N3s-A&ZR3t@mchacks2017.c5se38qdaeio.us-east-1.rds.amazonaws.com:3306/mchacks'


# Creating Database
db = SQLAlchemy(app)
migrate = Migrate(app, db)
server = Server(host="0.0.0.0", port=int(os.environ['PORT']))


manager = Manager(app)
manager.add_command('db', MigrateCommand)
manager.add_command("runserver", Server(),threaded=True,debug=True)


# Base.metadata.create_all(db)


@app.before_request
def check_id():
    print request
    if request.method == 'POST':
        sess_id = request.args['sessionId']
        var = User.filter_by(session_id = sess_id).all()

        user = User.filter_by(session_id = sess_id).all()
        if len(user) == 0:
            create_new_user(sess_id)
        else:
            gauss_clf = session.query(Classifiers).filter_by(user_id=user[0].id).first()


@app.route('/testdatabase', methods = ["POST"] )
def testdatabase():
    if request.method == "POST":
        id = request.args['ID']
        session_id = request.args['SESS_ID']
        user = User(session_id=session_id)
        db.session.add(user)
        db.session.commit()
        return "HAHAHA"

@app.route('/testdatabase2',methods = ["POST"])
def testdatabase2():
    dictionary_obj = {"Hello World":"This is me","HAHA":"HAHA"}
    if request.method == "POST":
        # Example of adding a pickled object
        user_id = request.form['user_id']
        classifier = Classifiers(user_id=user_id,pickled_classifier=dictionary_obj)
        db.session.add(classifier)
        db.session.commit()
        return "WORKED"


@app.route('/gettest_pickled')
def testdatabase3():
    results = Classifiers.query.all()
    qar = [ result.pickled_classifier   for result in results]
    print(qar)
    return "HEHE"

        

@app.route('/homepage')
def homepage():
    # JINJA
    users = [1,2,3,4,5]
    return render_template("index.html",dictionary={"users":users})

@app.route('/', methods =["POST"] )
def get_con():
    if request.method == "POST":
        json_text = json.dumps({"id": request.args['sessionId']})
        return json_text

@app.after_request
def header(response):
    response.headers['Content-type'] = ' application/json'
    return response

def create_new_user(sess_id):
    gauss_clf = GaussianNB()
    user = User(session_id=sess_id)
    db.session.add(user)
    user_id = User.filter_by(session_id = sess_id).all()[0].id
    classifier = Classifiers(user_id=user_id,pickled_classifier=gauss_clf)
    db.session.add(classifier)
    db.session.commit()

if __name__ == "__main__":
    manager.run()
