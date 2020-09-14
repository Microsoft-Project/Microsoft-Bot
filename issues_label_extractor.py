import numpy as np
from pymongo import MongoClient

client = MongoClient('mongodb://localhost:27017')
db = client['github']


class IssueLabel:
    @staticmethod
    def get_labels(collection):
        if 'trending_repo_names' and 'issues' in collection:
            trending_repo_names = db.get_collection(
                'trending_repo_names'
            ).aggregate(
                [
                    {
                        '$lookup': {
                            'from': 'issues',
                            'localField': 'name',
                            'foreignField': 'repo',
                            'as': 'array',
                        },
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

            issue_labels = []
            repo_companies = []

            for pull_requests in trending_repo_names:
                if len(pull_requests['array']['labels']) > 0:
                    issue_labels.append(pull_requests['array']['labels'])
                    repo_companies.append(pull_requests['name'])

            # TODO: See if we can get rid of these variables
            #   Why don't we extract the names directly?
            new_repo_companies = []
            labels = []
            i = 0
            for lists in issue_labels:
                for list_item in lists:
                    labels.append(list_item['name'])
                    new_repo_companies.append(repo_companies[i])
                i += 1

            num_array = np.array([])
            for i in range(len(repo_companies)):
                temp = np.array([[new_repo_companies[i], labels[i]]])
                num_array = np.append(num_array, temp)

            num_array = num_array.reshape(int((num_array.size / 2)), 2)

            return num_array
