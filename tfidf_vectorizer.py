from sklearn.feature_extraction.text import TfidfVectorizer
import pandas as pd
import pickle

listings = pd.read_csv("listings.csv")


descriptions =  listings["description"].tolist()

cleanedList = [x for x in descriptions if str(x) != 'nan']

vec = TfidfVectorizer()

vec.fit(cleanedList)
#
# x = vec.get_feature_names()
# print x

pickle.dumps("vectorizer.pkl")



