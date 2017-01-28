@app.route('/testdatabase', methods = ["POST"] )
def testdatabase():
    if request.method == "POST":
        id = request.args['ID']
        session_id = request.args['SESS_ID']
        user = User(session_id=session_id)
        session = Session()
        session.add(user)
        session.commit()
        return "HAHAHA"

@app.route('/testdatabase2',methods = ["POST"])
def testdatabase2():
    dictionary_obj = {"Hello World":"This is me","HAHA":"HAHA"}
    if request.method == "POST":
        # Example of adding a pickled object
        user_id = request.form['user_id']
        classifier = Classifiers(user_id=user_id,pickled_classifier=dictionary_obj)
        session = Session()
        session.add(classifier)
        session.commit()
        return "WORKED"


@app.route('/gettest_pickled')
def testdatabase3():
    session = Session()
    results = session.query(Classifiers).all()
    qar = [ result.pickled_classifier   for result in results]
    print(qar)
    return "HEHE"