import numpy as np
from pymongo import MongoClient

client = MongoClient('mongodb://localhost:27017')
db = client['github']


class RepoLabel:
    @staticmethod
    def get_labels(collection):
        if 'trending_repo_names' and 'repo_labels' in collection:
            repo_labels = db.get_collection('trending_repo_names').aggregate(
                [
                    {
                        '$lookup': {
                            'from': 'repo_labels',
                            'localField': 'name',
                            'foreignField': 'repo',
                            'as': 'array',
                        },
                    },
                    {'$unwind': '$array'},
                    {
                        '$project': {
                            'array.name': True,
                            'name': True,
                            '_id': False,
                        }
                    },
                ]
            )

            label_names = []
            repo_companies = []

            for repo_label in repo_labels:
                label_names.append(repo_label['array']['name'])
                repo_companies.append(repo_label['name'])

            num_array = np.array([])
            for i in range(len(repo_companies)):
                temp = np.array([[repo_companies[i], label_names[i]]])
                num_array = np.append(num_array, temp)

            num_array = num_array.reshape(int((num_array.size / 2)), 2)

            return num_array
