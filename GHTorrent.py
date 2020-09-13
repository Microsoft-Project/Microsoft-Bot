import time
import numpy as np
from pymongo import MongoClient
from PyDictionary import PyDictionary

from repo_label_extractor import repo_label_extractor
from pull_request_label_extractor import pullRequestLabels
from issues_label_extractor import issueLabels

client = MongoClient('mongodb://localhost:27017')
db = client['github']

collections = db.list_collection_names()


# print(collections)

def updateTrendings(collectionsList):
    if "Trendings" in collectionsList:
        # drop the old trending repos data
        db.drop_collection("Trendings")
        time.sleep(2)
    if 'repos' in collectionsList:
        # query the new trending repos
        trendings_repos = db.get_collection('repos').find(
            {'fork': False,
             '$or': [{'stargazers_count': {'$gte': 1000}},
                     {'watchers_count': {'$gte': 1000}}]})
        # creating the new collection with data
        db.create_collection('Trendings')
        db['Trendings'].insert_many(trendings_repos)
    else:
        print('There is no source from to get new Data from ')


def updateTrendNames(collectionsList):
    if "Trend_repo_names" in collectionsList:
        # drop the old trending repos data
        db.drop_collection("Trend_repo_names")
        time.sleep(2)

    if 'Trendings' in collectionsList:

        trending_names = db.get_collection('Trendings').distinct("name")
        db.create_collection('Trend_repo_names')
        for obj in trending_names:
            db['Trend_repo_names'].insert_one({'name': obj})
    else:
        print('There are no trending repos collection')


def populate_label_data(collectionsList, np_list1,np_list2,np_list3):
    if "Trending_Labels" in collectionsList:
        db.drop_collection("Trending_Labels")
        time.sleep(2)

    db.create_collection("Trending_Labels")
    size_List1 = np_list1.shape[0]
    for i in range(size_List1):
        tuple = {'company': np_list1[i:i + 1, 0][0], 'label': np_list1[i:i + 1, 1][0]}
        db['Trending_Labels'].insert_one(tuple)

    size_List2 = np_list2.shape[0]
    for i in range(size_List2):
        tuple = {'company': np_list2[i:i + 1, 0][0], 'label': np_list2[i:i + 1, 1][0]}
        db['Trending_Labels'].insert_one(tuple)

    size_List3 = np_list3.shape[0]
    for i in range(size_List3):
        tuple = {'company': np_list3[i:i + 1, 0][0], 'label': np_list3[i:i + 1, 1][0]}
        db['Trending_Labels'].insert_one(tuple)


# Uncomment the following only when want to update or create the Trending Collection
# updateTrendings(collections)
# time.sleep(2)
# updateTrendNames(collections)


# label extraction from the repo_labels collection from dump data
repo_labels_ex = repo_label_extractor()
repo_labels = repo_labels_ex.extractLabels(collections)

# label extraction from dump data pull requests
pull_request_ex = pullRequestLabels()
pull_labels = pull_request_ex.queryRepoNames(collections)

# label extraction from dump issues
issue_ex = issueLabels()
issue_labels = issue_ex.extractlabels(collections)

# print(repo_labels.shape, pull_labels.shape, issue_labels.shape)
# print(repo_labels, '\n', pull_labels, '\n', issue_labels)

# populate the table with Labels
populate_label_data(collections, repo_labels, pull_labels, issue_labels)

print('done')
