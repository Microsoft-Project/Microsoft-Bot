import pprint
import numpy as np
from pymongo import MongoClient
from PyDictionary import PyDictionary

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


### Call Only the following when want to update the trendings
# updateTrendings(collections)
# updateTrendNames(collections)


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
count = 0
for obj in query:
    nameList.append(obj['array']['name'])

# print(nameList)

nameList = list(dict.fromkeys(nameList))

print(nameList)

#
# dictionary=PyDictionary()
#
#
# for vars in singleVars:
#     print(vars, '    ', dictionary.synonym(vars))



print('done')
