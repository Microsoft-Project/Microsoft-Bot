import numpy as np
from pymongo import MongoClient

client = MongoClient('mongodb://localhost:27017')
db = client['github']


class PullRequestLabel:
    @staticmethod
    def get_labels(collection):
        if 'trending_repos' and 'pull_requests' in collection:
            trending_repos = db.get_collection('trending_repos').aggregate(
                [
                    {
                        '$lookup': {
                            'from': 'pull_requests',
                            'localField': 'name',
                            'foreignField': 'repo',
                            'as': 'array',
                        }
                    },
                    {'$unwind': '$array'},
                    {
                        '$project': {
                            'array.labels': True,
                            'name': True,
                            '_id': False,
                        }
                    },
                ],
            )

            repo_prs = []
            repo_companies = []

            for list_pull_requests in trending_repos:
                if len(list_pull_requests['array']['labels']) > 0:
                    repo_prs.append(list_pull_requests['array']['labels'])
                    repo_companies.append(list_pull_requests['name'])

            nameList = []
            newComp = []
            i = 0
            for lists in repo_prs:
                for obj in lists:
                    nameList.append(obj['name'])
                    newComp.append(repo_companies[i])
                i += 1

            num_array = np.array([])
            for i in range(len(repo_companies)):
                temp = np.array([[newComp[i], nameList[i]]])
                num_array = np.append(num_array, temp)

            num_array = num_array.reshape(int((num_array.size / 2)), 2)

            return num_array
        else:
            print('Trend_repo_names or pull_requests are missing ....')
