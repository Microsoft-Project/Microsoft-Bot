import pprint
import numpy as np
from pymongo import MongoClient
from PyDictionary import PyDictionary

client = MongoClient('mongodb://localhost:27017')
db = client['github']

collections = db.list_collection_names()


class pullRequestLabels:

    def queryRepoNames(self):
        query = db.get_collection('Trend_repo_names').aggregate([
            {'$lookup':
                {
                    'from': 'pull_requests',
                    'localField': 'name',
                    'foreignField': 'repo',
                    'as': 'array'
                }
            },
            {'$unwind': '$array'},
            {'$project': {'array.labels': True, '_id': False}}
        ])

        pullList = []
        nameList=[]
        for list_pull_requests in query:
            if len(list_pull_requests['array']['labels']) > 0 :
                pullList.append(list_pull_requests['array']['labels'])

        for lists in pullList:
            for obj in lists:
                nameList.append(obj["name"])
        return nameList

