import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns
from sklearn.feature_extraction.text import TfidfVectorizer


def get_top_features_cluster(tf_idf_array, prediction, n_feats, corpus):
    vectorizer = TfidfVectorizer()
    vectorizer.fit_transform(corpus)
    labels = np.unique(prediction)
    dfs = []
    for label in labels:
        id_temp = np.where(prediction == label)  # indices for each cluster
        x_means = np.mean(tf_idf_array[id_temp], axis=0)  # returns average score across cluster
        sorted_means = np.argsort(x_means)[::-1][:n_feats]  # indices with top 20 scores
        features = vectorizer.get_feature_names()
        best_features = [(features[i], x_means[i]) for i in sorted_means]
        df = pd.DataFrame(best_features, columns=['features', 'score'])
        dfs.append(df)
    return dfs


def plotWords(dfs, n_feats):
    plt.figure(figsize=(8, 4))
    for i in range(0, len(dfs)):
        plt.title(("Most Common Words in Cluster {}".format(i)), fontsize=10, fontweight='bold')
        sns.barplot(x='score', y='features', orient='h', data=dfs[i][:n_feats])
        plt.show()
