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

    if 'Trendings' in collectionsList:

        trending_names = db.get_collection('Trendings').distinct("name")
        db.create_collection('Trend_repo_names')
        for obj in trending_names:
            db['Trend_repo_names'].insert_one({'name': obj})
    else:
        print('There are no trending repos collection')

def populate_label_data (np_list):
    print()

### Uncomment the following only when want to update or create the Trending Collection
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

print(repo_labels.shape, pull_labels.shape, issue_labels.shape)
print(repo_labels, '\n', pull_labels, '\n', issue_labels)

#populate the table with Labels
populate_label_data(repo_labels)
populate_label_data(pull_labels)
populate_label_data(issue_labels)


print('done')
