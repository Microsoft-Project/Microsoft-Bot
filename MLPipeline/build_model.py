import pandas as pd
import os
import pickle

import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.feature_selection import chi2
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.naive_bayes import MultinomialNB
from sklearn.svm import LinearSVC

import Evaluation.model_metrics as eval

dirname = os.path.dirname(__file__).replace('/MLPipeline', '')


def build_save(model_type):
    try:
        tfidf, features, labels, category_to_id, df = get_datafeatures()
    except Exception:
        return

    N = 2
    for LABEL, category_id in sorted(category_to_id.items()):
        features_chi2 = chi2(features, labels == category_id)
        indices = np.argsort(features_chi2[0])
        feature_names = np.array(tfidf.get_feature_names())[indices]
        unigrams = [v for v in feature_names if len(v.split(' ')) == 1]
        bigrams = [v for v in feature_names if len(v.split(' ')) == 2]
        print("# '{}':".format(LABEL))
        print("  . Most correlated unigrams:\n. {}".format('\n. '.join(unigrams[-N:])))
        print("  . Most correlated bigrams:\n. {}".format('\n. '.join(bigrams[-N:])))
    X_train, X_test, y_train, y_test = train_test_split(df['body_title'], df['labels'], random_state=1)
    count_vect = CountVectorizer()
    X_train_counts = count_vect.fit_transform(X_train.values.astype('U'))
    tfidf_transformer = TfidfTransformer()
    X_train_tfidf = tfidf_transformer.fit_transform(X_train_counts)
    filename_vec = os.path.join(dirname, 'Models/vec_1.pkl')
    filename_mod = os.path.join(dirname, 'Models/mod_1.pkl')
    print(filename_mod)

    pickle.dump(count_vect, open(
        filename_vec, "wb"))

    if model_type is 'lgr':
        model = LogisticRegression()
        lgr = model.fit(X_train_tfidf, y_train)
        pickle.dump(lgr, open(
            filename_mod, "wb"))
        eval.confu_gen("lgr", features, labels, 0.3, df)

    elif model_type is 'rfc':
        model = RandomForestClassifier()
        rfc = model.fit(X_train_tfidf, y_train)
        pickle.dump(rfc, open(
            filename_mod, "wb"))
        eval.confu_gen("forest", features, labels, 0.3, df)

    elif model_type is 'mnb':
        model = MultinomialNB()
        mnb = model.fit(X_train_tfidf, y_train)
        pickle.dump(mnb, open(
            filename_mod, "wb"))
        eval.confu_gen("mnb", features, labels, 0.3, df)

    elif model_type is 'lvc':
        model = LinearSVC()
        lvc = model.fit(X_train_tfidf, y_train)
        pickle.dump(lvc, open(
            filename_mod, "wb"))
        eval.confu_gen("lsvc", features, labels, 0.3, df)


def get_datafeatures():
    filename_data_proc = os.path.join(dirname, 'Dataset/Jan20/Processed/processed_latest_balanced.csv')
    print(filename_data_proc)
    try:
        df = pd.read_csv(
            filename_data_proc)
    except:
        print('\nData file is not present, please upload a dataset first, then retry\n')
        raise Exception('FileNotFound')

    col = ['body_title', 'labels', 'category_id']
    df = df[col]
    df.columns = ['body_title', 'labels', 'category_id']
    text_label = df['labels'].tolist()
    category_id_df = df[['labels', 'category_id']].drop_duplicates().sort_values('category_id')
    category_to_id = dict(category_id_df.values)
    # id_to_category = dict(category_id_df[['category_id', 'labels']].values)
    tfidf = TfidfVectorizer()
    features = tfidf.fit_transform(df['body_title'].values.astype('U')).toarray()
    labels = df.category_id
    print(features.shape[0])

    return tfidf, features, labels, category_to_id, df
