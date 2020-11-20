import requests
import corpus_processor as cp
import clustering as cluster
import analyse_cluster as ac


def fetch_issue_data(repo_full_name):
    comment_list = []
    for i in range(1, 6):
        req = requests.get(
            f'https://api.github.com/repos/{repo_full_name}/issues?state=all&since=2000-01-01T00:00:00Z&per_page=100&page=' + str(
                i))
        for doc in get_data_from_json(req):
            comment_list.append(doc)

    return comment_list


def get_data_from_json(json_data):
    """
    Returns list containing only 'body' from issue comments.

    :param json_data: json input from Github API
    :return: list
    """
    tmp_arr = []

    for i in json_data.json():
        tmp_arr.append(i['body'])

    return tmp_arr


processed_corpus = cp.processCorpus(fetch_issue_data('material-components/material-components-android'), 'english')

print(processed_corpus)

print('-----------')

final_df = cluster.get_tfidf(processed_corpus)

k = 8
kmeans_results = cluster.run_KMeans(k, final_df)

cluster.silhouette(kmeans_results, final_df, plot=True)

best_result = 2
kmeans = kmeans_results.get(best_result)

final_df_array = final_df.to_numpy()
prediction = kmeans.predict(final_df)
n_feats = 20
dfs = ac.get_top_features_cluster(final_df_array, prediction, n_feats, processed_corpus)
ac.plotWords(dfs, 10)
