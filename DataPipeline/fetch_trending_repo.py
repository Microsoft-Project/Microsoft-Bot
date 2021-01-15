from pymongo import MongoClient

client = MongoClient('mongodb://localhost:27017')
db = client['github']

collections = db.list_collection_names()


def update_trending_repos_collection(trending_repos_list):
    if 'trending_repos' in trending_repos_list:
        # drop old trending_repos collection
        db.drop_collection('trending_repos')
    if 'repos' in trending_repos_list:
        # query new trending_repos collection
        trending_repos = db.get_collection('repos').find(
            {
                'fork': False,
                '$or': [
                    {'stargazers_count': {'$gte': 500}},
                    {'watchers_count': {'$gte': 500}},
                ],
            },
        )

        # create new collection with data
        db.create_collection('trending_repos')
        db['trending_repos'].insert_many(trending_repos)
    else:
        print('No collection with name "trending_repos" found!')


def update_trending_repo_names_collection(trending_repo_names_list):
    if 'trending_repo_names' in trending_repo_names_list:
        # drop the old trending repos data
        db.drop_collection('trending_repo_names')
    if 'trending_repos' in trending_repo_names_list:
        trending_repo_names = db.get_collection('trending_repos').distinct(
            'full_name'
        )
        db.create_collection('trending_repo_names')

        for trending_repo_name in trending_repo_names:
            db['trending_repo_names'].insert_one({'full_name': trending_repo_name})
    else:
        print('There are no trending repos collection')
