import time

from pymongo import MongoClient

from repo_label_extractor import RepoLabel
from issues_label_extractor import IssueLabel
from pull_request_label_extractor import PullRequestLabel

client = MongoClient('mongodb://localhost:27017')
db = client['github']

collections = db.list_collection_names()


def update_trending_repos_collection(trending_repos_list):
    if 'trending_repos' in trending_repos_list:
        # drop old trending_repos collection
        db.drop_collection('trending_repos')
        time.sleep(2)
    if 'repos' in trending_repos_list:
        # query new trending_repos collection
        trending_repos = db.get_collection('repos').find(
            {
                'fork': False,
                '$or': [
                    {'stargazers_count': {'$gte': 1000}},
                    {'watchers_count': {'$gte': 1000}},
                ],
            },
        )

        # create new collection with data
        db.create_collection('trending_repos')
        db['trending_repos'].insert_many(trending_repos)
    else:
        print('No collection with name "trending_repos" found!')


def update_trending_repo_names_collection(trending_repo_names_list):
    if 'trending_repo_names' in trending_repo_names_list:
        # drop the old trending repos data
        db.drop_collection('trending_repo_names')
        time.sleep(2)
    if 'trending_repos' in trending_repo_names_list:
        trending_repo_names = db.get_collection('trending_repos').distinct(
            'name'
        )
        db.create_collection('trending_repo_names')

        for trending_repo_name in trending_repo_names:
            db['trending_repo_names'].insert_one({'name': trending_repo_name})
    else:
        print('There are no trending repos collection')


def populate_label_data(trending_labels, np_list_1, np_list_2, np_list_3):
    if 'trending_labels' in trending_labels:
        db.drop_collection('trending_labels')
        time.sleep(2)

    db.create_collection('trending_labels')
    for i in range(get_list_size(np_list_1)):
        # Todo: Avoid shadowing built-in types!!
        tuple = {
            'company': np_list_1[i : i + 1, 0][0],
            'label': np_list_1[i : i + 1, 1][0],
        }
        db['trending_labels'].insert_one(tuple)

    for i in range(get_list_size(np_list_2)):
        tuple = {
            'company': np_list_2[i : i + 1, 0][0],
            'label': np_list_2[i : i + 1, 1][0],
        }
        db['trending_labels'].insert_one(tuple)

    for i in range(get_list_size(np_list_3)):
        tuple = {
            'company': np_list_3[i : i + 1, 0][0],
            'label': np_list_3[i : i + 1, 1][0],
        }
        db['trending_labels'].insert_one(tuple)


def get_list_size(np_list):
    return np_list.shape[0]


# only run when updating or creating 'trending_repos' collection
# update_trending_repos_collection(collections)
# time.sleep(2)
# update_trending_repo_names_collection(collections)

# get repo labels
repo_labels = RepoLabel.get_labels(collections)

# get labels from repo pull requests
pr_labels = PullRequestLabel.get_labels(collections)

# get labels from repo issues
issue_labels = IssueLabel.get_labels(collections)

# print(repo_labels.shape, pull_labels.shape, issue_labels.shape)
# print(repo_labels, '\n', pull_labels, '\n', issue_labels)

# populate the table with Labels
populate_label_data(collections, repo_labels, pr_labels, issue_labels)

# print('done')
