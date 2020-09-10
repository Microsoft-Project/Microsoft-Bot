import pprint
import numpy as np
from pymongo import MongoClient
from PyDictionary import PyDictionary

client = MongoClient('mongodb://localhost:27017')
db = client['github']

class repo_label_extractor:

    def extractLabels(self, collectionList):
        if 'Trend_repo_names' and 'repo_labels' in collectionList:
            query = db.get_collection('Trend_repo_names').aggregate([
                {'$lookup':
                    {
                        'from': 'repo_labels',
                        'localField': 'name',
                        'foreignField': 'repo',
                        'as': 'array'
                    }
                },
                {'$unwind': '$array'},
                {'$project': {'array.name': True, '_id': False}}
            ])
            nameList = []
            for obj in query:
                nameList.append(obj['array']['name'])

            nameList = list(dict.fromkeys(nameList))

            return nameList

