from sklearn.naive_bayes import GaussianNB
import cPickle


def recommend():
    with open('clf.pkl', 'rb') as f:
        vectorizer = cPickle.load(f)