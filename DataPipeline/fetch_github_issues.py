import pandas as pd
import requests

TRENDING_REPO = "Upload trending repo file name here"


def fetch_issue_data(repo_full_name, range_high, label):
    comment_list = []

    for i in range(1, range_high + 1):
        req = requests.get(
            f'https://api.github.com/repos/{repo_full_name}/issues?state=all&per_page=100&page=' + str(
                i) + "&labels=" + str(label))
        for whole in get_data_from_json(req, label):
            comment_list.append(whole)

    return comment_list


def get_data_from_json(json_data, label):
    """
    Returns list containing only 'body' from issue comments.

    :param json_data: json input from Github API
    :return: list
    """

    whole_array = []

    original_array = ['bug', 'enhancement', 'question']
    index = original_array.index(label)
    del original_array[index]

    for i in json_data.json():
        flag = 1
        labels_list = i['labels']
        list_names = []
        for lab in labels_list:
            list_names.append(lab['name'])
        for check in original_array:
            if check in list_names:
                flag = 0
        if flag is 1:
            whole_array.append([i['title'], i['body'], label])
            continue
        print(list_names)

    return whole_array


df = pd.read_csv(TRENDING_REPO)

toCall_list = df['full_name'].tolist()

final_issue_list = []

for repo in range(1, 5):
    reponame = toCall_list[repo]
    final_issue_list.append(fetch_issue_data(str(reponame), 1, 'bug'))
