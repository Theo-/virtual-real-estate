from sklearn.naive_bayes import GaussianNB
import pickle

def train_classifier():
    with open('vectorizer.pkl', 'rb') as f:
        vectorizer = pickle.load(f)
    x = vectorizer.get_feature_names()
    print x
train_classifier()