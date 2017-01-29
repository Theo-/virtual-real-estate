from sklearn.naive_bayes import GaussianNB
import pickle

def train_classifier(features,y ):
    with open('vectorizer.pkl', 'rb') as f:
        vectorizer = pickle.load(f)

    vectors =vectorizer.transform(features)

    clf = GaussianNB()

    clf.partial_fit(features,y)





