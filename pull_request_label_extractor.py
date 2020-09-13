import pprint
import numpy as np
from pymongo import MongoClient
from PyDictionary import PyDictionary

client = MongoClient('mongodb://localhost:27017')
db = client['github']

class pullRequestLabels:

    def queryRepoNames(self, collectionList):
        if 'Trend_repo_names' and 'pull_requests' in collectionList:

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
                {'$project': {'array.labels': True,'name': True, '_id': False}}
            ])

            pullList = []
            nameList=[]
            company = []

            for list_pull_requests in query:
                if len(list_pull_requests['array']['labels']) > 0:
                    company.append(list_pull_requests['name'])
                    pullList.append(list_pull_requests['array']['labels'])

            newComp = []
            i = 0
            for lists in pullList:
                for obj in lists:
                    nameList.append(obj["name"])
                    newComp.append(company[i])
                i += 1

            # nameList = list(dict.fromkeys(nameList))

            print(len(newComp))
            print(len(nameList))
            return nameList , newComp
        else:
            print('Trend_repo_names or pull_requests are missing ....')
