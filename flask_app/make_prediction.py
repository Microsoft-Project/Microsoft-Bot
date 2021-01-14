import corpus_processor as cp
import pickle
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.multiclass import OneVsRestClassifier
from sklearn.svm import LinearSVC

def load_model(file_name):
    return pickle.load(open(file_name, 'rb'))


def make_prediction(data):
    # model = OneVsRestClassifier(load_model('./model/lsvc3Labels2021.pkl'))
    model = load_model('./model/lsvc3Labels2021.pkl')
    processed_data = cp.processCorpusSingle(data)
    loaded_vec = pickle.load(open('model/vectorizer3label2021.pkl', 'rb'))


    prediction = model.predict(loaded_vec.transform([processed_data]))
    print(prediction)
    return processed_data, prediction
