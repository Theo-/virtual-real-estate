from sklearn.naive_bayes import GaussianNB
import cPickle

def recommend(clf, features):
    with open('vectorizer.pkl', 'rb') as f:
        vectorizer = cPickle.load(f)

    vectors =vectorizer.transform(features)

    return clf.predict(features)

