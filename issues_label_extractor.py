import pprint
import numpy as np
from pymongo import MongoClient
from PyDictionary import PyDictionary

client = MongoClient('mongodb://localhost:27017')
db = client['github']


class issueLabels:


    def extractLabels(self,collectionList):
        if 'Trend_repo_names' and 'issues' in collectionList:
            query = db.get_collection('Trend_repo_names').aggregate([
                {'$lookup':
                    {
                        'from': 'issues',
                        'localField': 'name',
                        'foreignField': 'repo',
                        'as': 'array'
                    }
                },
                {'$unwind': '$array'},
                {'$project': {'array.labels': True, '_id': False}}
            ])


            issuesList = []
            count = 0
            for list_pull_requests in query:
                if len(list_pull_requests['array']['labels']) > 0 :
                    issuesList.append(list_pull_requests['array']['labels'])

            print(issuesList)
            #
            labels = []
            for lists in issuesList:
                for obj in lists:
                    labels.append(obj['name'])


            for label in labels:
                print(label)